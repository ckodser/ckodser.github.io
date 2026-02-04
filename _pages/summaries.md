---
layout: page
title: Summaries
permalink: /summaries/
description: Paper summaries
nav: true
nav_order: 5
display_categories: [Reasoning, Hallucination, Interpretability, ActiveLearning]
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
  {% assign displayed_categories = page.display_categories %}
  {% assign uncategorized_list = "" | split: "" %}
    {% for project in site.summaries %}
    {% assign should_be_in_other = true %}
    {% if project.categories %}
      {% for project_category in project.categories %}
        {% if displayed_categories contains project_category %}
          {% assign should_be_in_other = false %}
        {% endif %}
      {% endfor %}
    {% endif %}
    {% if should_be_in_other %}
      {% assign uncategorized_list = uncategorized_list | push: project %}
    {% endif %}
  {% endfor %}
  {% assign sorted_uncategorized = uncategorized_list | sort: "importance" %}

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
