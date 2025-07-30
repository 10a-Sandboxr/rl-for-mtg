export default function Page() {
  const bib = `@misc{mtg-rl-2025,
  title={{Reinforcement Learning for Competitive Magic: The Gathering Gameplay}},
  author={{Alex Researcher and Blair Scientist and Casey Theorist and Dana Engineer}},
  year={{2025}},
  note={{Preprint}},
  howpublished={{Project webpage}}
}`.trim();

  return (
    <main className="container">
      <section className="card">
        <h1>Reinforcement Learning for Competitive <i>Magic: The Gathering</i> Gameplay</h1>
        <h2>Project Website</h2>
        <p className="meta">
          Alex Researcher (MIT) · Blair Scientist (Stanford) · Casey Theorist (CMU) · Dana Engineer (Oxford)
        </p>
        <p>
          We study self-play reinforcement learning for <i>Magic: The Gathering</i> (MTG), a partially observable, adversarial domain with a
          combinatorial action space and a rules engine built around priority and a LIFO stack. Our framework combines hierarchical action
          abstraction, model-based planning with search, and a population-based outer loop for deck optimization.
        </p>
        <div className="grid">
          <a className="btn" href="/downloads/reinforcement-learning-mtg-paper.zip">Download: Paper (LaTeX + BibTeX)</a>
          <span className="btn" aria-disabled="true" title="Coming soon">PDF (coming soon)</span>
          <a className="btn" href="#bibtex">Cite (BibTeX)</a>
        </div>
        <h3 style={{marginTop: '24px'}}>Abstract</h3>
        <p className="muted">
          MTG is a long-horizon, stochastic, partially observable, adversarial domain with a combinatorial action space and
          expressive rules. We propose a self-play RL framework that integrates a rules-faithful simulator with hierarchical
          action abstraction, model-based planning and search, and a population-driven outer loop for deck optimization, along
          with evaluation protocols reflecting the volatile metagame.
        </p>
        <h3>Contact</h3>
        <p className="muted">Email placeholders: alexr@example.edu, blairs@example.edu, caseyt@example.edu, danae@example.edu</p>
        <h3 id="bibtex">BibTeX</h3>
        <pre style={{whiteSpace:'pre-wrap', overflowX:'auto'}}>{bib}</pre>
      </section>
      <footer>
        © 2025 MTG RL Project • Deployed on Vercel
      </footer>
    </main>
  );
}