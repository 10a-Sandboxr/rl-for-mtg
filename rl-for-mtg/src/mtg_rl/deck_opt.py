
import random

def mutate_seed(seed: int) -> int:
    rng = random.Random(seed)
    return rng.randrange(10_000_000)

def evolve_seeds(pop_size=8, gens=5):
    seeds = [random.randrange(10_000_000) for _ in range(pop_size)]
    for _ in range(gens):
        seeds = sorted(seeds)[:pop_size//2] + [mutate_seed(s) for s in seeds[:pop_size//2]]
    return seeds
