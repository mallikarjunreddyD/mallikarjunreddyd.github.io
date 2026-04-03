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
  </aside>
</section>

<section class="home-bottom-grid">
  <div class="home-hero-card">
    <h3>Recent Updates</h3>
    <ul class="home-interest-list">
      <li>Conducted the Agentica 2.0, IdeaVerse'26, and Cosmix hackathons as part of Abhisarga 2026.</li>
      <li>Received the Best Paper Award at the 2024 IEEE International Conference on Advanced Networks and Telecommunications Systems.</li>
    </ul>
  </div>

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

  <div class="home-hero-card">
    <h3>Open to Collaborate</h3>
    <ul class="home-interest-list">
      <li>Academic collaborations in blockchain systems, secure distributed computing, and federated learning.</li>
      <li>Student projects, hackathons, workshops, and innovation-driven mentoring initiatives.</li>
      <li>Invited talks, interdisciplinary research discussions, and institutional partnerships.</li>
    </ul>
  </div>
</section>
