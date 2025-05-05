---
layout: page
title: Summaries
permalink: /summaries/
description: Paper summaries
nav: true
nav_order: 5
display_categories: [ActiveLearning, Interpretability]
horizontal: false
---

<!-- pages/summaries.md -->
<div class="projects">

<!-- Display categorized projects -->
  {% for category in page.display_categories %}
  <a id="{{ category }}" href=".#{{ category }}">
    <h2 class="category">{{ category }}</h2>
  </a>
 {% assign categorized_projects = site.summaries | where_exp: "item", "item.categories contains category" %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
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
  {% endfor %}
<h2 class="category">Other Summaries</h2>
{% assign uncategorized_projects = site.summaries | where_exp: "item", "item.categories == nil or item.categories.size == 0 or (item.categories | concat: page.display_categories | uniq | size) == (item.categories.size + page.display_categories.size)" %}
{% assign sorted_uncategorized = uncategorized_projects | sort: "importance" %}
{% if page.horizontal %}
<div class="container">
  <div class="row row-cols-1 row-cols-md-2">
  {% for project in sorted_uncategorized %}
    {% include projects_horizontal.liquid %}
  {% endfor %}
  </div>
</div>
{% else %}
<div class="row row-cols-1 row-cols-md-3">
  {% for project in sorted_uncategorized %}
    {% include projects.liquid %}
  {% endfor %}
</div>
{% endif %}
</div>