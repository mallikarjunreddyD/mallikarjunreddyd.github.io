---
layout: default
title: Home
---

{% assign a = site.author %}

<table>
<tr>
<td width="70%">

I am an academic and researcher working in the areas of blockchain systems,
federated learning, and decentralized architectures.

My research focuses on building scalable, transparent, and trustless systems
for next-generation digital infrastructure.

**Research interests**

- Blockchain systems
- Federated learning
- Decentralized finance
- Distributed systems

<p>
  <a href="{{ site.baseurl }}/assets/cv.pdf">Curriculum Vitae</a>
  {% if a.google_scholar %}
  | <a href="{{ a.google_scholar }}">Google Scholar</a>
  {% endif %}
  | <a href="https://github.com/{{ a.github_username }}">GitHub</a>
  {% if a.email %}
  | <a href="mailto:{{ a.email }}">Email</a>
  {% endif %}
</p>

</td>

<td width="30%" valign="top">
<img src="{{ site.baseurl }}/assets/profile.jpg" width="180" alt="Portrait of {{ site.title }}">
</td>
</tr>
</table>

---

## Recent updates

- Conducted Web3 Summer School and Solidity Bootcamp
- Developing XComb platform
- Working on blockchain-enabled federated learning
