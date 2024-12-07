---
layout: page
title: Summaries
permalink: /summaries/
description: Paper summaries
nav: true
nav_order: 5
display_categories: [Summary]
horizontal: false
---

<!-- pages/summaries.md -->
<div class="projects">
<!-- Display projects without categories -->

{% assign sorted_projects = site.summaries | sort: "importance" %}

  <!-- Generate cards for each project -->

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
</div>