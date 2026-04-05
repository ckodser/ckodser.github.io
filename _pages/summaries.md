---
layout: page
title: Summaries
permalink: /summaries/
description: Paper summaries
nav: true
nav_order: 5
display_categories: [autoformalization, Reasoning, Hallucination, Interpretability, ActiveLearning]
horizontal: false
---

<!-- pages/summaries.md -->
<div class="projects">

<!-- Autoformalization comparison tables -->
{% assign af_papers = site.summaries | where_exp: "item", "item.categories contains 'autoformalization'" %}
{% if af_papers.size > 0 %}
<style>
.af-overview h3 { margin-top: 1.5rem; margin-bottom: 0.75rem; font-size: 1.1rem; color: var(--global-theme-color); }
.af-comparison-table { font-size: 0.85rem; }
.af-comparison-table thead th { background-color: #f0f0f0; color: #212529; white-space: nowrap; vertical-align: bottom; }
.af-comparison-table td:first-child, .af-comparison-table th:first-child { min-width: 170px; }
.af-check { position: relative; color: #28a745; font-weight: bold; font-size: 1rem; cursor: help; }
.af-check[data-tooltip]::after {
  content: attr(data-tooltip);
  position: absolute;
  top: 130%; left: 50%;
  transform: translateX(-50%);
  background: #333; color: #fff;
  padding: 5px 9px; border-radius: 4px;
  font-size: 0.75rem; font-weight: normal;
  width: 230px; white-space: normal; text-align: left;
  pointer-events: none; visibility: hidden; opacity: 0;
  z-index: 9999;
}
.af-check[data-tooltip]:hover::after { visibility: visible; opacity: 1; }
.af-empty { color: #dee2e6; }
.badge-input { background-color: #6c757d; color: #fff; }
.badge-output { background-color: #28a745; color: #fff; }
.badge-input, .badge-output { font-size: 0.8rem; padding: 0.3em 0.6em; border-radius: 0.25rem; white-space: nowrap; }
.af-comparison-table td, .af-comparison-table th { color: #212529; }
</style>
<div class="af-overview">
  <a id="autoformalization-overview" href=".#autoformalization-overview">
    <h2 class="category" data-toggle="collapse" data-target="#af-overview-content" aria-expanded="false" aria-controls="af-overview-content" style="cursor:pointer">
      Autoformalization: Comparative Overview <small style="font-size:0.6em; color:#888">▶ expand</small>
    </h2>
  </a>

  <div id="af-overview-content" class="collapse">
  <h3>Input &amp; Output</h3>
  <div class="table-responsive">
    <table class="table table-sm table-bordered af-comparison-table">
      <thead>
        <tr>
          <th>Paper</th>
          <th>Input</th>
          <th>Output</th>
        </tr>
      </thead>
      <tbody>
        {% for paper in af_papers %}
        {% if paper.af_input or paper.af_output %}
        <tr>
          <td><a href="{{ paper.url | relative_url }}">{{ paper.af_short_title | default: paper.title }}</a></td>
          <td><span class="badge badge-input">{{ paper.af_input | default: "—" }}</span></td>
          <td><span class="badge badge-output">{{ paper.af_output | default: "—" }}</span></td>
        </tr>
        {% endif %}
        {% endfor %}
      </tbody>
    </table>
  </div>

  <h3>Agents Used</h3>
  <div class="table-responsive">
    <table class="table table-sm table-bordered text-center af-comparison-table">
      <thead>
        <tr>
          <th class="text-left">Paper</th>
          {% for agent in site.data.autoformalization_taxonomy.agents %}
          <th>{{ agent.name }}</th>
          {% endfor %}
        </tr>
      </thead>
      <tbody>
        {% for paper in af_papers %}
        {% if paper.af_agents %}
        <tr>
          <td class="text-left"><a href="{{ paper.url | relative_url }}">{{ paper.af_short_title | default: paper.title }}</a></td>
          {% for agent in site.data.autoformalization_taxonomy.agents %}
          <td>{% if paper.af_agents contains agent.id %}{% assign note = paper.af_agent_notes[agent.id] %}<span class="af-check" {% if note %}data-tooltip="{{ note }}"{% endif %}>✓</span>{% else %}<span class="af-empty">·</span>{% endif %}</td>
          {% endfor %}
        </tr>
        {% endif %}
        {% endfor %}
      </tbody>
    </table>
  </div>

  <h3>Tools &amp; MCPs Available</h3>
  <div class="table-responsive">
    <table class="table table-sm table-bordered text-center af-comparison-table">
      <thead>
        <tr>
          <th class="text-left">Paper</th>
          {% for tool in site.data.autoformalization_taxonomy.tools %}
          <th>{{ tool.name }}</th>
          {% endfor %}
        </tr>
      </thead>
      <tbody>
        {% for paper in af_papers %}
        {% if paper.af_tools %}
        <tr>
          <td class="text-left"><a href="{{ paper.url | relative_url }}">{{ paper.af_short_title | default: paper.title }}</a></td>
          {% for tool in site.data.autoformalization_taxonomy.tools %}
          <td>{% if paper.af_tools contains tool.id %}{% assign tnote = paper.af_tool_notes[tool.id] %}<span class="af-check" {% if tnote %}data-tooltip="{{ tnote }}"{% endif %}>✓</span>{% else %}<span class="af-empty">·</span>{% endif %}</td>
          {% endfor %}
        </tr>
        {% endif %}
        {% endfor %}
      </tbody>
    </table>
  </div>

  <h3>Datasets Used</h3>
  <div class="table-responsive">
    <table class="table table-sm table-bordered text-center af-comparison-table">
      <thead>
        <tr>
          <th class="text-left">Paper</th>
          {% for dataset in site.data.autoformalization_taxonomy.datasets %}
          <th>{{ dataset.name }}</th>
          {% endfor %}
        </tr>
      </thead>
      <tbody>
        {% for paper in af_papers %}
        {% if paper.af_datasets %}
        <tr>
          <td class="text-left"><a href="{{ paper.url | relative_url }}">{{ paper.af_short_title | default: paper.title }}</a></td>
          {% for dataset in site.data.autoformalization_taxonomy.datasets %}
          <td>{% if paper.af_datasets contains dataset.id %}{% assign dnote = paper.af_dataset_notes[dataset.id] %}<span class="af-check" {% if dnote %}data-tooltip="{{ dnote }}"{% endif %}>✓</span>{% else %}<span class="af-empty">·</span>{% endif %}</td>
          {% endfor %}
        </tr>
        {% endif %}
        {% endfor %}
      </tbody>
    </table>
  </div>

  <h3>Statement Formalization Evaluation</h3>
  <div class="table-responsive">
    <table class="table table-sm table-bordered af-comparison-table">
      <thead>
        <tr>
          <th>Paper</th>
          <th>Evaluation Method</th>
        </tr>
      </thead>
      <tbody>
        {% for paper in af_papers %}
        {% if paper.af_statement_formalization_evaluation %}
        <tr>
          <td><a href="{{ paper.url | relative_url }}">{{ paper.af_short_title | default: paper.title }}</a></td>
          <td>{{ paper.af_statement_formalization_evaluation }}</td>
        </tr>
        {% endif %}
        {% endfor %}
      </tbody>
    </table>
  </div>
  </div><!-- end collapse -->
</div>
<script>
(function() {
  var el = document.getElementById('af-overview-content');
  var label = document.querySelector('[data-target="#af-overview-content"] small');
  if (!el || !label) return;
  el.addEventListener('show.bs.collapse', function() { label.textContent = '▼ collapse'; });
  el.addEventListener('hide.bs.collapse', function() { label.textContent = '▶ expand'; });
})();
</script>
{% endif %}

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
