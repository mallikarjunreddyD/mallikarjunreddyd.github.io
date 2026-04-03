---
layout: default
title: Home
description: Official academic website of Dorsala Mallikarjun Reddy, Assistant Professor at IIIT Sri City, featuring research, teaching, publications, projects, events, and contact details.
---

{% assign a = site.author %}

<section class="home-hero">
  <div class="home-hero-copy">
    <p class="home-kicker">Blockchain Systems | Distributed Computing | Applied Research</p>
    <h2>Building trustworthy digital infrastructure for next-generation systems.</h2>
    <p class="home-summary">
      I am an academic and researcher working across blockchain systems, zero-knowledge
      proofs, federated learning, and decentralized architectures. My work focuses on
      scalable, transparent, and practically deployable systems for real-world digital platforms.
    </p>

    <div class="home-actions">
      <a class="landing-button" href="{{ site.baseurl }}/assets/cv.pdf">Curriculum Vitae</a>
      {% if a.google_scholar %}
      <a class="landing-button" href="{{ a.google_scholar }}">Google Scholar</a>
      {% endif %}
      <a class="landing-button" href="https://github.com/{{ a.github_username }}">GitHub</a>
      {% if a.email %}
      <a class="landing-button" href="mailto:{{ a.email }}">Email</a>
      {% endif %}
    </div>
  </div>

  <aside class="home-hero-panel">
    <img class="home-hero-photo" src="{{ site.baseurl }}/assets/profile.jpg" alt="Portrait of {{ site.title }}">

    <div class="home-hero-card">
      <h3>Research Interests</h3>
      <ul class="home-interest-list">
        <li>Blockchain systems</li>
        <li>Zero-knowledge proofs</li>
        <li>Federated learning</li>
        <li>Decentralized finance</li>
        <li>Distributed systems</li>
      </ul>
    </div>
  </aside>
</section>

<section class="home-highlights" aria-label="Highlights">
  <div class="home-highlight-card">
    <strong>Academic</strong>
    <span>Assistant Professor at IIIT Sri City with active teaching, mentoring, and institutional leadership roles.</span>
  </div>
  <div class="home-highlight-card">
    <strong>Research</strong>
    <span>Focused on blockchain networks, verifiable computation, federated systems, and secure distributed infrastructure.</span>
  </div>
  <div class="home-highlight-card">
    <strong>Practice</strong>
    <span>Industry experience in blockchain architecture and sustained involvement in workshops, hackathons, and applied innovation.</span>
  </div>
</section>

{% include landing-sections.html %}

<section class="home-updates">
  <h2>Recent Updates</h2>
  <div class="home-updates-grid">
    <article class="home-update-card">
      <h3>Web3 Training</h3>
      <p>Conducted Web3 Summer School and Solidity Bootcamp initiatives with a focus on hands-on learning and ecosystem building.</p>
    </article>
    <article class="home-update-card">
      <h3>Current Development</h3>
      <p>Developing XComb and related systems that bridge research ideas with practical platform implementation.</p>
    </article>
    <article class="home-update-card">
      <h3>Ongoing Research</h3>
      <p>Advancing work on blockchain-enabled federated learning and trustworthy decentralized computation.</p>
    </article>
  </div>
</section>
