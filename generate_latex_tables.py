import os
import re
import yaml

BASE = os.path.dirname(os.path.abspath(__file__))
TAXONOMY_FILE = os.path.join(BASE, '_data', 'autoformalization_taxonomy.yml')
SUMMARIES_DIR = os.path.join(BASE, '_summaries')


def parse_front_matter(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()
    if not content.startswith('---'):
        return {}
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def cite_key(title):
    key = re.sub(r'\(.*?\)', '', title)
    key = key.strip()
    key = re.sub(r' +', '_', key)
    return key


def latex_escape(text):
    text = text.replace('\\', r'\textbackslash{}')
    text = text.replace('&', r'\&')
    text = text.replace('%', r'\%')
    text = text.replace('$', r'\$')
    text = text.replace('#', r'\#')
    text = text.replace('_', r'\_')
    text = text.replace('{', r'\{')
    text = text.replace('}', r'\}')
    text = text.replace('~', r'\textasciitilde{}')
    text = text.replace('^', r'\^{}')
    return text


with open(TAXONOMY_FILE) as f:
    taxonomy = yaml.safe_load(f)

agents = taxonomy['agents']
tools = taxonomy['tools']

papers = []
for fname in sorted(os.listdir(SUMMARIES_DIR)):
    if not fname.endswith('.md'):
        continue
    fm = parse_front_matter(os.path.join(SUMMARIES_DIR, fname))
    if not fm:
        continue
    if 'autoformalization' not in fm.get('categories', []):
        continue
    papers.append(fm)

papers.sort(key=lambda p: p.get('importance', 999))


def paper_cell(p):
    short = p.get('af_short_title', p['title'])
    ck = cite_key(short)
    return rf'{latex_escape(short)}~\cite{{{ck}}}'


def table1():
    lines = [
        r'\begin{table}[h]',
        r'\centering',
        r'\begin{tabular}{lll}',
        r'\toprule',
        r'Paper & Input & Output \\',
        r'\midrule',
    ]
    for p in papers:
        inp = latex_escape(p.get('af_input', '---'))
        out = latex_escape(p.get('af_output', '---'))
        lines.append(rf'{paper_cell(p)} & {inp} & {out} \\')
    lines += [
        r'\bottomrule',
        r'\end{tabular}',
        r'\caption{Input \& Output comparison of autoformalization papers}',
        r'\end{table}',
    ]
    return '\n'.join(lines)


def table2():
    col_spec = 'l' + 'c' * len(agents)
    agent_headers = ' & '.join(latex_escape(a['name']) for a in agents)
    lines = [
        r'\begin{table}[h]',
        r'\centering',
        r'\resizebox{\textwidth}{!}{%',
        rf'\begin{{tabular}}{{{col_spec}}}',
        r'\toprule',
        rf'Paper & {agent_headers} \\',
        r'\midrule',
    ]
    for p in papers:
        af_agents = p.get('af_agents', [])
        cells = [r'\checkmark' if a['id'] in af_agents else '' for a in agents]
        lines.append(rf'{paper_cell(p)} & {" & ".join(cells)} \\')
    lines += [
        r'\bottomrule',
        r'\end{tabular}',
        r'}',
        r'\caption{Agents used in autoformalization papers}',
        r'\end{table}',
    ]
    return '\n'.join(lines)


def table3():
    col_spec = 'l' + 'c' * len(tools)
    tool_headers = ' & '.join(latex_escape(t['name']) for t in tools)
    lines = [
        r'\begin{table}[h]',
        r'\centering',
        r'\resizebox{\textwidth}{!}{%',
        rf'\begin{{tabular}}{{{col_spec}}}',
        r'\toprule',
        rf'Paper & {tool_headers} \\',
        r'\midrule',
    ]
    for p in papers:
        af_tools = p.get('af_tools', [])
        cells = [r'\checkmark' if t['id'] in af_tools else '' for t in tools]
        lines.append(rf'{paper_cell(p)} & {" & ".join(cells)} \\')
    lines += [
        r'\bottomrule',
        r'\end{tabular}',
        r'}',
        r'\caption{Tools \& MCPs available in autoformalization papers}',
        r'\end{table}',
    ]
    return '\n'.join(lines)


print("% ===== Table 1: Input & Output =====")
print(table1())
print()
print("% ===== Table 2: Agents Used =====")
print(table2())
print()
print("% ===== Table 3: Tools & MCPs =====")
print(table3())
