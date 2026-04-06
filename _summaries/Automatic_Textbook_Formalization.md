---
layout: page
title: Automatic Textbook Formalization
description: A multi-agent framework utilizing code-capable language models to translate and prove graduate-level mathematical textbooks in the Lean theorem prover.
categories: [autoformalization]
img: assets/img/Automatic_Textbook_Formalization/main_image.svg
importance: 1
giscus_comments: true
link: https://arxiv.org/pdf/2604.03071v1
af_short_title: "Textbook Formalizer"
af_input: "NLP Document"
af_output: "Formal Statement + Formal Proof"
af_agents: [formal_statement, formal_prover, semantic_check, engineering_reviewer, maintainer, triage, scanner, progress]
af_tools: [file_system, lean4_mcp, theorem_search, git_tools, bash_tool, issue_tracker]
af_datasets: [textbook]
af_dataset_notes:
    textbook: "Introduction to Algebraic Combinatorics by Darij Grinberg (~500 pages, 340 target theorems/definitions). Chosen for being largely disjoint from existing Mathlib coverage."
af_statement_formalization_evaluation: "Post-run, an interactive blueprint website enables human community verification side-by-side. No quantitative metric for statement accuracy is reported."
af_tool_notes:
  file_tools: "List, read (with line ranges), write, edit (string replacement or line-range replacement), delete, and grep across the project. Write access excludes .tex, .md, .pdf, .txt files. Reviewer agents get read-only access."
  lean4_mcp: "Centralized pool of persistent Lean 4 REPL instances with Mathlib preloaded. Agents send code snippets and receive OK or detailed error messages with goal states. Much faster than lake build for iterative proof development."
  theorem_search: "Three tools: mathlib_grep (ripgrep regex search across Mathlib source, filterable by declaration kind), mathlib_find_name (exact or fuzzy declaration name search), mathlib_read_file (read Mathlib source with line ranges). Enables discovery of existing lemmas and APIs."
  git_tools: "Agents operate in isolated git worktrees. Restricted commands: status, add, commit, diff, log, rebase, restore, checkout_file. Write access constrained to the agent's own branch."
  bash_tool: "Sandboxed shell with an allowlist of safe commands: lake (Lean build system), text processing (cat, grep, sed, awk), file navigation. Dangerous commands (rm -rf, curl, network access) blocked by SafeShell validator."
  issue_tracker: "File-system-based issue tracking (YAML in ISSUES.md). Agents can create_issue (with description and origin) and list_issues (filtered by status). Enables asynchronous coordination between agent roles."
af_agent_notes:
  formal_statement: "Receives chapter-level LaTeX source and translates all definitions and theorem statements into Lean declarations with sorry placeholders. Acts as the statement formalizer, aligning naming with Mathlib conventions. ~85 deployed."
  formal_prover: "Takes a specific sorry theorem and constructs a complete formal proof using Mathlib tactics and the Lean REPL for interactive checking. Escalates blockers by creating issues or proposing statement fixes. ~8,704 deployed."
  semantic_check: "Read-only agent reviewing PRs for mathematical correctness. Checks semantic faithfulness of formalized statements against source material and proof completeness. Renders APPROVE, REQUEST_CHANGES, REJECT, or ABSTAIN. ~6,797 deployed."
  engineering_reviewer: "Read-only agent reviewing PRs for code quality: naming conventions, formatting, documentation, compilation success. Both reviewers must approve (AND-success policy) for a PR to merge. ~6,805 deployed."
  maintainer: "Resolves open issues: missing definitions, incorrect statements, refactoring, dependency problems. Can add helper lemmas, fix upstream declarations, restructure code. Repository-wide scope (up to 14 files). ~6,467 deployed."
  triage: "Periodically reviews open issues, identifies resolved or obsolete ones, and closes them with explanations. Keeps the issue tracker clean for maintainers. ~550 deployed."
  scanner: "Periodically scans the codebase for architectural issues: code duplication, API gaps, forward dependencies, naming inconsistencies. Creates issues for maintainers. ~307 deployed."
  progress: "Tracks target theorem completion to prevent the system from derailing onto non-target work. ~331 deployed."
---

## Method

The formalization system treats proof construction as a software engineering task and uses a multi-agent scaffold based on a command-line interface. The system relies on standard collaborative software engineering practices, utilizing `git` for version control, a trunk-based development model with short-lived feature branches, continuous integration (CI), and a file-system-based issue tracker.

The pipeline isolates specific tasks by deploying concurrent sub-agents with well-defined roles:
*   **Sketcher agents**: Process chunks of the source material (e.g., chapters) to generate Lean formalizations of definitions and theorem statements. Proofs are omitted using the `sorry` keyword.
*   **Prover agents**: Receive theorems containing `sorry` statements and attempt to construct complete Lean proofs. They can also directly resolve or escalate issues regarding missing helpers or incorrect statement formalizations.
*   **Reviewer agents**: Evaluate pull requests (PRs) submitted by sketcher and prover agents. Reviews are divided into a *mathematical review* (verifying semantic equivalence to the source text) and an *engineering review* (checking formatting, naming conventions, and API design). PRs require approval from both reviewers, a successful merge without conflicts, and a passing repository build.
*   **Maintainer agents**: Process active files in the issue tracker to unblock formalization paths, often refactoring code or writing helper lemmas.
*   **Triage agents**: Assess open issues to determine if they have been resolved by other PRs and mark them accordingly.
*   **Scan and Progress agents**: Monitor the repository for global engineering issues (e.g., code duplication, mismatched conventions) and track the completion status of the designated target theorems.

Agents are granted access to predefined tools:
*   **File tools**: Functions to read chunks, edit via line numbers or search-and-replace, and list files.
*   **Lean tools**: Snippet execution using the Lean REPL, `mathlib` file/declaration search, and `grep` utilities.
*   **Git tools**: Restricted version control commands (`status`, `add`, `commit`, `rebase`, `diff`) limiting write access to an agent's specific branch.
*   **Bash tool**: An allowed list of shell commands for text processing (`cat`, `awk`, `grep`) and Lean compilation (`lake`).
*   **Issue tracker tools**: Utilities to create and list issues using UUIDs.

## Experiments

The system was evaluated on a 500-page graduate-level algebraic combinatorics textbook. The source text was selected due to its conceptual reliance on, but lack of direct inclusion in, Lean's `mathlib`. To quantify completion, 340 specific theorems and definitions were manually labeled as targets.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Automatic_Textbook_Formalization/image2.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

The experiment ran on eight machines distributing the build processes, with git status synchronized via a shared Network File System (NFS) directory.

**Results and Volume**
The formalization resolved all 340 target theorems and definitions over a runtime of one week. The final output consisted of roughly 130,000 lines of Lean code and 5,900 Lean declarations.
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Automatic_Textbook_Formalization/image1.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Automatic_Textbook_Formalization/image4.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



**Agent Execution and Outcomes**
The orchestration utilized approximately 30,000 agents. Execution tokens totaled 83 billion for input and 561 million for output.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Automatic_Textbook_Formalization/image5.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Automatic_Textbook_Formalization/image6.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



Of the executed agents, Provers and Maintainers accounted for the majority of actions and token consumption. Agents modifying files submitted PRs that were constrained in size, generally hovering around 100 net lines of code.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Automatic_Textbook_Formalization/image7.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Automatic_Textbook_Formalization/image8.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>





**Cost Estimation Calculation**
Total compute costs were modeled using prompt caching parameters. Assuming $$N$$ agents, $$T$$ average turns per agent, $$m$$ average token length per turn, and $$C$$ total tokens processed in inputs:

$$
C = Nm \sum_{i=1}^{T} i = Nm \frac{T(T + 1)}{2}
$$

$$
m = \frac{2C}{NT(T + 1)}
$$

$$
L = Tm = \frac{2C}{N(T + 1)}
$$

Using this cache ratio, the estimated inference cost for the entire textbook completion was approximately $100,000.

**System Dynamics and Failures**
While Prover agents exclusively modified isolated Lean files, Maintainer agents executed repository-wide tasks impacting up to 14 files concurrently.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Automatic_Textbook_Formalization/image9.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



During execution, specific coherence and process failures were observed:
*   **Semantic Duplication**: An $$N$$-partition data type was defined three separate times by different agents, requiring later refactoring to build a shared definition and prove equivalence between APIs.
*   **Mathematical Inconsistencies**: Formalizations of informal combinatorial definitions (e.g., Bender-Knuth involutions) yielded competing definitions that failed on global proofs, causing Prover agents to identify counterexamples but fail to implement a root-cause refactor.
*   **Task Derailment**: Agents occasionally ignored directives and initiated extensive proofs for standard cited theorems (e.g., constructing Pfaffians for domino tilings) instead of relying on external references.
*   **Infrastructure Bottlenecks**: The shared NFS directory and the single-threaded merge queue produced timeouts and high resource contention during peak parallelization.
