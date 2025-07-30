export default function Page() {
  const bib = `@misc{mtg-rl-2025,
  title={{Reinforcement Learning for Competitive Magic: The Gathering Gameplay}},
  author={{Alex Thaikanov and Blair Probst and Casey Tzao  and Dana Evelyn}},
  year={{2025}},
  note={{Preprint}},
  howpublished={{Project webpage}}
}`.trim();

  return (
    <main className="container">
      <section className="card">
        <h1>Reinforcement Learning for Competitive <i>Magic: The Gathering</i> Gameplay</h1>
        <h2>Research Project Website</h2>
        <p className="meta">
          Alex Thaikanov (MIT) · Blair Probst (Stanford) · Casey Tzao (CMU) · Dana Evelyn (Oxford)
        </p>

        <form method="get" action="/downloads/MTG_with_RL.pdf">
          <button type="submit" className="cta">Download the Paper</button>
        </form>

        <div className="badges">
          <span className="badge"><i>●</i> Self‑play RL</span>
          <span className="badge"><i>●</i> Hierarchical actions for stack & priority</span>
          <span className="badge"><i>●</i> Model‑based planning + search</span>
          <span className="badge"><i>●</i> Population training & deck co‑evolution</span>
          <span className="badge"><i>●</i> Rigorous evaluation (ELO, matchup matrix)</span>
        </div>

        <p>
          <b>Reinforcement learning for Magic: The Gathering</b> is our central focus. MTG combines hidden information, a long time horizon,
          and a combinatorial action space shaped by the game’s priority windows and LIFO stack. These ingredients make MTG a
          uniquely demanding testbed for decision‑making under uncertainty, beyond what is typically captured by perfect‑information
          board games or short‑horizon video games.
        </p>

        <div className="section">
          <h3>What this paper proposes</h3>
          <p>
            We introduce a self‑play reinforcement learning framework that marries a rules‑faithful simulator with <b>hierarchical
            action abstraction</b>, enabling agents to reason at the level of “intents” (e.g., hold up interaction, execute a combo)
            while grounding those choices in the full, grammar‑constrained set of legal plays. On top of that, we incorporate
            <b> model‑based planning</b>—a MuZero‑style latent dynamics model coupled with tree search—to improve timing and targeting
            decisions around the stack. To avoid brittle specializations, training proceeds in a <b>population</b> with a
            <b> co‑evolving metagame</b>, where decks and policies improve together.
          </p>
        </div>

        <div className="section grid">
          <div>
            <h3>Method at a glance</h3>
            <ol>
              <li>Encode public state, private hand, and stack as permutation‑invariant sets and sequences.</li>
              <li>Choose <em>intents</em> that gate a tractable subset of legal actions at each priority window.</li>
              <li>Plan in a learned latent space with MCTS to refine policy and value estimates.</li>
              <li>Train via self‑play across a diverse opponent population (current + historical checkpoints).</li>
              <li>Co‑optimize decklists in an outer loop to reflect—and pressure‑test—the evolving metagame.</li>
            </ol>
          </div>
          <div>
            <h3>Why MTG is a stress test</h3>
            <ul>
              <li>Hidden hands & randomized draws (partial observability).</li>
              <li>Spikes in branching factor at timing windows (priority / stack responses).</li>
              <li>Combinatorial actions (attack/block subsets, multi‑target spells, modes & costs).</li>
              <li>Non‑stationary objectives due to rotating sets and shifting metagames.</li>
            </ul>
          </div>
        </div>

        <div className="section">
          <h3>Abstract)</h3>
          <p className="muted">
            We develop a rules‑aware, self‑play RL system for MTG that integrates hierarchical actions, model‑based planning
            with search, and population training coupled to deck co‑evolution. We outline evaluation protocols (ELO, matchup matrix,
            generalization to unseen decks) and ablations that isolate how search budget, abstraction, and population diversity drive strength.
          </p>
        </div>

        <div className="section" id="bibtex">
          <h3>Cite</h3>
          <pre style={{whiteSpace:'pre-wrap', overflowX:'auto'}}>{bib}</pre>
        </div>

        <footer>
          © 2025 MTG RL Project
        </footer>
      </section>
    </main>
  );
}