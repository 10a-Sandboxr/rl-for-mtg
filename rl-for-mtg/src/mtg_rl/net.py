
import torch
import torch.nn as nn

class PolicyValueNet(nn.Module):
    def __init__(self, action_dim: int):
        super().__init__()
        self.backbone = nn.Sequential(
            nn.Linear(64, 128), nn.ReLU(),
            nn.Linear(128, 128), nn.ReLU(),
        )
        self.policy = nn.Linear(128, action_dim)
        self.value = nn.Linear(128, 1)

    def forward(self, x):
        h = self.backbone(x)
        p = self.policy(h)
        v = self.value(h).tanh()
        return p, v

def featurize(obs: dict) -> torch.Tensor:
    me = obs["me"]; opp = obs["opp"]
    vec = []
    vec += [float(obs["turn"]), float(obs["phase"])]
    vec += [float(me["life"]), float(me["lands_in_play"]), float(len(me["hand"])), float(len(me["battlefield"])), float(len(me["graveyard"])), float(me["library_count"])]
    vec += [float(opp["life"]), float(opp["lands_in_play"]), float(opp["hand_count"]), float(len(opp["battlefield"])), float(len(opp["graveyard"])), float(opp["library_count"])]
    while len(vec) < 64:
        vec.append(0.0)
    import torch
    return torch.tensor(vec[:64], dtype=torch.float32).unsqueeze(0)
