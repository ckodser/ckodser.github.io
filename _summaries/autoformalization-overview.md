---
layout: page
title: "Autoformalization: Comparative Overview"
description: Side-by-side comparison of autoformalization papers across agents, tools, datasets, and evaluation methods.
categories: [autoformalization]
importance: 0
img: assets/img/autoformalization-overview/banner.svg
---

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
.af-other-cell { text-align: left !important; min-width: 180px; }
.af-other-badge {
  position: relative;
  display: inline-block;
  background-color: #6c757d;
  color: #fff;
  font-size: 0.72rem;
  padding: 0.2em 0.5em;
  border-radius: 0.25rem;
  margin: 0.1em;
  cursor: help;
  white-space: nowrap;
}
.af-other-badge[data-tooltip]::after {
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
.af-other-badge[data-tooltip]:hover::after { visibility: visible; opacity: 1; }
</style>

{% assign af_papers = site.summaries | where_exp: "item", "item.categories contains 'autoformalization'" %}
{% assign af_papers = af_papers | where_exp: "item", "item.url != page.url" %}

<div class="af-overview">

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
{% assign agent_main_sort = "" %}
{% assign agent_other_ids = "" %}
{% for agent in site.data.autoformalization_taxonomy.agents %}
  {% assign acount = 0 %}
  {% for paper in af_papers %}
    {% if paper.af_agents contains agent.id %}{% assign acount = acount | plus: 1 %}{% endif %}
  {% endfor %}
  {% if acount >= 3 %}
    {% assign ainv = 99 | minus: acount %}
    {% capture asort_entry %}{{ ainv | prepend: "00" | slice: -2, 2 }}:{{ forloop.index0 | prepend: "00" | slice: -2, 2 }}:{{ agent.id }}{% endcapture %}
    {% assign asort_entry = asort_entry | strip %}
    {% unless agent_main_sort == "" %}{% assign agent_main_sort = agent_main_sort | append: "," %}{% endunless %}
    {% assign agent_main_sort = agent_main_sort | append: asort_entry %}
  {% else %}
    {% if acount > 0 %}
      {% unless agent_other_ids == "" %}{% assign agent_other_ids = agent_other_ids | append: "," %}{% endunless %}
      {% assign agent_other_ids = agent_other_ids | append: agent.id %}
    {% endif %}
  {% endif %}
{% endfor %}
{% assign sorted_agents = agent_main_sort | split: "," | sort %}
{% assign other_agent_ids = agent_other_ids | split: "," %}
<div class="table-responsive">
  <table class="table table-sm table-bordered text-center af-comparison-table">
    <thead>
      <tr>
        <th class="text-left">Paper</th>
        {% for entry in sorted_agents %}
        {% assign eparts = entry | split: ":" %}
        {% assign eid = eparts[2] %}
        {% assign edata = site.data.autoformalization_taxonomy.agents | where: "id", eid | first %}
        <th>{{ edata.name }}</th>
        {% endfor %}
        {% if agent_other_ids != "" %}<th class="text-left">Other</th>{% endif %}
      </tr>
    </thead>
    <tbody>
      {% for paper in af_papers %}
      {% if paper.af_agents %}
      <tr>
        <td class="text-left"><a href="{{ paper.url | relative_url }}">{{ paper.af_short_title | default: paper.title }}</a></td>
        {% for entry in sorted_agents %}
        {% assign eparts = entry | split: ":" %}
        {% assign eid = eparts[2] %}
        <td>{% if paper.af_agents contains eid %}{% assign note = paper.af_agent_notes[eid] %}<span class="af-check" {% if note %}data-tooltip="{{ note }}"{% endif %}>&#x2713;</span>{% else %}<span class="af-empty">&middot;</span>{% endif %}</td>
        {% endfor %}
        {% if agent_other_ids != "" %}
        <td class="af-other-cell">
          {% for oid in other_agent_ids %}
            {% if paper.af_agents contains oid %}
              {% assign odata = site.data.autoformalization_taxonomy.agents | where: "id", oid | first %}
              {% assign onote = paper.af_agent_notes[oid] %}
              <span class="af-other-badge"{% if onote %} data-tooltip="{{ onote | escape }}"{% endif %}>{{ odata.name }}</span>
            {% endif %}
          {% endfor %}
        </td>
        {% endif %}
      </tr>
      {% endif %}
      {% endfor %}
    </tbody>
  </table>
</div>

<h3>Tools &amp; MCPs Available</h3>
{% assign tool_main_sort = "" %}
{% assign tool_other_ids = "" %}
{% for tool in site.data.autoformalization_taxonomy.tools %}
  {% assign tcount = 0 %}
  {% for paper in af_papers %}
    {% if paper.af_tools contains tool.id %}{% assign tcount = tcount | plus: 1 %}{% endif %}
  {% endfor %}
  {% if tcount >= 2 %}
    {% assign tinv = 99 | minus: tcount %}
    {% capture tsort_entry %}{{ tinv | prepend: "00" | slice: -2, 2 }}:{{ forloop.index0 | prepend: "00" | slice: -2, 2 }}:{{ tool.id }}{% endcapture %}
    {% assign tsort_entry = tsort_entry | strip %}
    {% unless tool_main_sort == "" %}{% assign tool_main_sort = tool_main_sort | append: "," %}{% endunless %}
    {% assign tool_main_sort = tool_main_sort | append: tsort_entry %}
  {% else %}
    {% if tcount > 0 %}
      {% unless tool_other_ids == "" %}{% assign tool_other_ids = tool_other_ids | append: "," %}{% endunless %}
      {% assign tool_other_ids = tool_other_ids | append: tool.id %}
    {% endif %}
  {% endif %}
{% endfor %}
{% assign sorted_tools = tool_main_sort | split: "," | sort %}
{% assign other_tool_ids = tool_other_ids | split: "," %}
<div class="table-responsive">
  <table class="table table-sm table-bordered text-center af-comparison-table">
    <thead>
      <tr>
        <th class="text-left">Paper</th>
        {% for entry in sorted_tools %}
        {% assign tparts = entry | split: ":" %}
        {% assign tid = tparts[2] %}
        {% assign tdata = site.data.autoformalization_taxonomy.tools | where: "id", tid | first %}
        <th>{{ tdata.name }}</th>
        {% endfor %}
        {% if tool_other_ids != "" %}<th class="text-left">Other</th>{% endif %}
      </tr>
    </thead>
    <tbody>
      {% for paper in af_papers %}
      {% if paper.af_tools %}
      <tr>
        <td class="text-left"><a href="{{ paper.url | relative_url }}">{{ paper.af_short_title | default: paper.title }}</a></td>
        {% for entry in sorted_tools %}
        {% assign tparts = entry | split: ":" %}
        {% assign tid = tparts[2] %}
        <td>{% if paper.af_tools contains tid %}{% assign tnote = paper.af_tool_notes[tid] %}<span class="af-check" {% if tnote %}data-tooltip="{{ tnote }}"{% endif %}>&#x2713;</span>{% else %}<span class="af-empty">&middot;</span>{% endif %}</td>
        {% endfor %}
        {% if tool_other_ids != "" %}
        <td class="af-other-cell">
          {% for oid in other_tool_ids %}
            {% if paper.af_tools contains oid %}
              {% assign odata = site.data.autoformalization_taxonomy.tools | where: "id", oid | first %}
              {% assign onote = paper.af_tool_notes[oid] %}
              <span class="af-other-badge"{% if onote %} data-tooltip="{{ onote | escape }}"{% endif %}>{{ odata.name }}</span>
            {% endif %}
          {% endfor %}
        </td>
        {% endif %}
      </tr>
      {% endif %}
      {% endfor %}
    </tbody>
  </table>
</div>

<h3>Datasets Used</h3>
{% assign dataset_main_sort = "" %}
{% assign dataset_other_ids = "" %}
{% for dataset in site.data.autoformalization_taxonomy.datasets %}
  {% assign dcount = 0 %}
  {% for paper in af_papers %}
    {% if paper.af_datasets contains dataset.id %}{% assign dcount = dcount | plus: 1 %}{% endif %}
  {% endfor %}
  {% if dcount >= 2 %}
    {% assign dinv = 99 | minus: dcount %}
    {% capture dsort_entry %}{{ dinv | prepend: "00" | slice: -2, 2 }}:{{ forloop.index0 | prepend: "00" | slice: -2, 2 }}:{{ dataset.id }}{% endcapture %}
    {% assign dsort_entry = dsort_entry | strip %}
    {% unless dataset_main_sort == "" %}{% assign dataset_main_sort = dataset_main_sort | append: "," %}{% endunless %}
    {% assign dataset_main_sort = dataset_main_sort | append: dsort_entry %}
  {% else %}
    {% if dcount > 0 %}
      {% unless dataset_other_ids == "" %}{% assign dataset_other_ids = dataset_other_ids | append: "," %}{% endunless %}
      {% assign dataset_other_ids = dataset_other_ids | append: dataset.id %}
    {% endif %}
  {% endif %}
{% endfor %}
{% assign sorted_datasets = dataset_main_sort | split: "," | sort %}
{% assign other_dataset_ids = dataset_other_ids | split: "," %}
<div class="table-responsive">
  <table class="table table-sm table-bordered text-center af-comparison-table">
    <thead>
      <tr>
        <th class="text-left">Paper</th>
        {% for entry in sorted_datasets %}
        {% assign dparts = entry | split: ":" %}
        {% assign did = dparts[2] %}
        {% assign ddata = site.data.autoformalization_taxonomy.datasets | where: "id", did | first %}
        <th>{{ ddata.name }}</th>
        {% endfor %}
        {% if dataset_other_ids != "" %}<th class="text-left">Other</th>{% endif %}
      </tr>
    </thead>
    <tbody>
      {% for paper in af_papers %}
      {% if paper.af_datasets %}
      <tr>
        <td class="text-left"><a href="{{ paper.url | relative_url }}">{{ paper.af_short_title | default: paper.title }}</a></td>
        {% for entry in sorted_datasets %}
        {% assign dparts = entry | split: ":" %}
        {% assign did = dparts[2] %}
        <td>{% if paper.af_datasets contains did %}{% assign dnote = paper.af_dataset_notes[did] %}<span class="af-check" {% if dnote %}data-tooltip="{{ dnote }}"{% endif %}>&#x2713;</span>{% else %}<span class="af-empty">&middot;</span>{% endif %}</td>
        {% endfor %}
        {% if dataset_other_ids != "" %}
        <td class="af-other-cell">
          {% for oid in other_dataset_ids %}
            {% if paper.af_datasets contains oid %}
              {% assign odata = site.data.autoformalization_taxonomy.datasets | where: "id", oid | first %}
              {% assign onote = paper.af_dataset_notes[oid] %}
              <span class="af-other-badge"{% if onote %} data-tooltip="{{ onote | escape }}"{% endif %}>{{ odata.name }}</span>
            {% endif %}
          {% endfor %}
        </td>
        {% endif %}
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

</div>
