# Reinforcement Learning for Competitive Magic: The Gathering — Research Repo

**Authors:** Alex Thaikanov (MIT), Blair Probst (Stanford), Casey Tzao (CMU), Dana Evelyn (Oxford)

This is the official implementation of the paper "Reinforcement Learning for Competitive Magic: The Gathering" (NeurIPS 2025)

---

## Overview

A compact, end‑to‑end research codebase for studying **reinforcement learning (RL) in Magic: The Gathering (MTG)** using a simplified but rules‑aware environment (**MiniMTG**), **PUCT‑style MCTS**, and a **policy/value network**. The repository also includes a minimal one‑page website to present the project and artifacts.

- **Problem:** MTG is long‑horizon, partially observable, and highly combinatorial.
- **Approach:** Self‑play RL with a lightweight **MiniMTG** environment, **MCTS** planning, and a compact **MLP policy/value** model.
- **Goal:** Provide a **reproducible reference** that’s easy to run, ablate, and extend into richer rules / metagame dynamics.

---

## Repository Contents

- **Website (Next.js)**: Project landing page in the repo root (`app/`, `public/`).
- **RL Codebase (Python)**: `rl-for-mtg/src/` directory with environment, MCTS, model, and training loop.

