
import os, random, json
import torch
import torch.nn.functional as F
import torch.optim as optim
from .net import PolicyValueNet, featurize
from .selfplay import self_play_episode

class ReplayBuffer:
    def __init__(self, capacity=10000):
        self.buf = []
        self.capacity = capacity

    def push(self, item):
        self.buf.append(item)
        if len(self.buf) > self.capacity:
            self.buf.pop(0)

    def sample(self, bs):
        import random
        return random.sample(self.buf, min(bs, len(self.buf)))

def train(run_dir="runs/exp1", episodes=50, action_dim=64, sims=64, seed=0, device="cpu"):
    os.makedirs(run_dir, exist_ok=True)
    torch.manual_seed(seed); random.seed(seed)

    net = PolicyValueNet(action_dim=action_dim).to(device)
    opt = optim.Adam(net.parameters(), lr=1e-3)

    rb = ReplayBuffer(20000)

    for ep in range(episodes):
        traces, outcome = self_play_episode(net, simulations=sims, seed=seed+ep)
        for obs, a, r in traces:
            x = featurize(obs)
            pi = torch.zeros(action_dim); pi[0] = 1.0
            rb.push((x.squeeze(0), pi, outcome))

        for _ in range(16):
            batch = rb.sample(64)
            if not batch: break
            X = torch.stack([b[0] for b in batch]).to(device)
            P = torch.stack([b[1] for b in batch]).to(device)
            Z = torch.tensor([b[2] for b in batch], dtype=torch.float32, device=device).unsqueeze(1)
            logits, v = net(X)
            policy_loss = F.kl_div(F.log_softmax(logits, dim=1), P, reduction='batchmean')
            value_loss = F.mse_loss(v, Z)
            loss = policy_loss + value_loss
            opt.zero_grad(); loss.backward(); opt.step()

        metrics = {"episode": ep+1, "buffer": len(rb.buf), "outcome": float(outcome)}
        print(json.dumps(metrics))
        if (ep+1) % 10 == 0:
            torch.save(net.state_dict(), os.path.join(run_dir, f"model_ep{ep+1}.pt"))

    torch.save(net.state_dict(), os.path.join(run_dir, "model_final.pt"))
    with open(os.path.join(run_dir, "metrics.json"), "w") as f:
        json.dump({"episodes": episodes}, f)

if __name__ == "__main__":
    train()
