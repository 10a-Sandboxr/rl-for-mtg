
from mtg_rl.env import MiniMTGEnv

def test_env_runs():
    env = MiniMTGEnv(seed=123)
    for _ in range(10):
        legal = env.legal_actions()
        assert len(legal) > 0
        obs, r, done, _ = env.step(legal[0])
        if done:
            break
