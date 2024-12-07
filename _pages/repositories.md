---
layout: page
permalink: /repositories/
title: repositories
description: Repositories to which I'm a major contributor. Most of these works were done as a course final project.
nav: true
nav_order: 3
---

{% if site.data.repositories.github_repos %}

## GitHub Repositories

<div class="repositories d-flex flex-wrap flex-md-row flex-column justify-content-between align-items-center">
  {% for repo in site.data.repositories.github_repos %}
    {% include repository/repo.liquid repository=repo %}
  {% endfor %}
</div>
{% endif %}
