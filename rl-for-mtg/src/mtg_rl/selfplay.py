
from __future__ import annotations
import copy
import torch
from typing import List, Tuple, Any, Dict
from .env import MiniMTGEnv
from .net import PolicyValueNet, featurize
from .mcts import MCTS

def enumerate_actions(env: MiniMTGEnv):
    return env.legal_actions()

def step_clone(env: MiniMTGEnv, action):
    e2 = copy.deepcopy(env)
    obs, r, done, _ = e2.step(action)
    return e2, obs, r, done

def policy_value_from_net(net: PolicyValueNet, env: MiniMTGEnv):
    obs = env._observe()
    acts = enumerate_actions(env)
    x = featurize(obs)
    with torch.no_grad():
        logits, v = net(x)
        probs = torch.softmax(logits, dim=1).squeeze(0)
    priors = []
    for i, a in enumerate(acts):
        j = i % probs.shape[0]
        priors.append((a, float(probs[j])))
    return priors, float(v.squeeze(0))

def self_play_episode(net: PolicyValueNet, simulations: int = 64, seed: int = 0):
    env = MiniMTGEnv(seed=seed)
    mcts = MCTS(lambda obs: policy_value_from_net(net, env), simulations=simulations)
    traces = []
    while True:
        obs = env._observe()
        legal = env.legal_actions()
        if not legal:
            break
        def legal_actions_fn(_): return legal
        def step_fn(_s, a):
            e2, o2, r, d = step_clone(env, a)
            return o2, r, d
        a = mcts.run(obs, legal_actions_fn, step_fn)
        pre_obs = obs
        _, r, done, _ = env.step(a)
        traces.append((pre_obs, a, r))
        if done:
            break
    outcome = traces[-1][2] if traces else 0.0
    return traces, outcome
