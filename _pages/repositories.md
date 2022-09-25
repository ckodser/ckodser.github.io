---
layout: page
permalink: /repositories/
title: repositories
description: Repositories which I'm a main contributor. Most of these works done as a course final project. 
nav: true
nav_order: 3
---

## GitHub Repositories

{% if site.data.repositories.github_repos %}
<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.html repository=repo %}
  {% endfor %}
</div>
{% endif %}
