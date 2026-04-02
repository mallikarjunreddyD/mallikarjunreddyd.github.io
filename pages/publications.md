---
layout: default
title: Publications
permalink: /pages/publications.html
---

{% assign groups = site.data.scholar_publications %}

{% if groups and groups.size > 0 %}
  {% for g in groups %}
    <h2>{{ g.year }}</h2>
    <ul>
      {% for p in g.publications %}
        <li>
          {% if p.authors %}{{ p.authors }}. {% endif %}
          {% if p.title %}"{{ p.title }}"{% endif %}
          {% if p.venue %}, {{ p.venue }}{% endif %}.
          {% if p.url %} <a href="{{ p.url }}" target="_blank" rel="noopener">[link]</a>{% endif %}
        </li>
      {% endfor %}
    </ul>
  {% endfor %}
{% else %}
  <p>No publications data found yet.</p>
  <p>
    To auto-fill from your Google Scholar profile, run:
    <code>python3 scripts/update_scholar_publications.py</code>
  </p>
{% endif %}