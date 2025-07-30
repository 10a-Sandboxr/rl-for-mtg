
import math
from typing import Dict, List, Tuple, Any, Optional, Callable

class Node:
    def __init__(self, prior: float = 0.0):
        self.N = 0
        self.W = 0.0
        self.Q = 0.0
        self.P = prior
        self.children: Dict[str, 'Node'] = {}
        self.action: Optional[Any] = None

class MCTS:
    def __init__(self, policy_value_fn: Callable[[dict], Tuple[List[Tuple[Any, float]], float]], c_puct: float = 1.5, simulations: int = 64):
        self.f = policy_value_fn
        self.c_puct = c_puct
        self.simulations = simulations

    def run(self, root_state, legal_actions_fn: Callable[[Any], List[Any]], step_fn: Callable[[Any, Any], Tuple[Any, float, bool]]):
        root = Node()
        priors, v = self.f(root_state)
        for a, p in priors:
            key = self._ak(a)
            nd = Node(prior=p)
            nd.action = a
            root.children[key] = nd

        for _ in range(self.simulations):
            path = [root]
            states = [root_state]
            node = root
            while node.children:
                key, node = self._select_child(node)
                s = states[-1]
                a = node.action
                ns, r, done = step_fn(s, a)
                states.append(ns)
                path.append(node)
                if done:
                    v_leaf = r
                    break
            else:
                priors, v_leaf = self.f(states[-1])
                for a, p in priors:
                    key = self._ak(a)
                    nd = Node(prior=p)
                    nd.action = a
                    node.children[key] = nd

            for i, n in enumerate(reversed(path)):
                n.N += 1
                n.W += v_leaf
                n.Q = n.W / n.N
                v_leaf = -v_leaf

        actions = [(child.N, child.action) for child in root.children.values()]
        actions.sort(reverse=True, key=lambda x: x[0])
        return actions[0][1] if actions else None

    def _select_child(self, node: Node):
        totalN = sum(ch.N for ch in node.children.values()) + 1
        best_key, best_node, best_score = None, None, -1e9
        for k, ch in node.children.items():
            u = self.c_puct * ch.P * math.sqrt(totalN) / (1 + ch.N)
            score = ch.Q + u
            if score > best_score:
                best_score = score; best_key = k; best_node = ch
        return best_key, best_node

    def _ak(self, a):
        return str(a)
