---
layout: page
title: Numina-Lean-Agent An Open and General Agentic Reasoning System for Formal Mathematics
description: A formal mathematical reasoning system that combines a general coding agent with specialized tools via the Model Context Protocol to interact with the Lean theorem prover.
categories: [autoformalization]
img: assets/img/Numina_Lean_Agent_An_Open_and_General_Agentic_Reasoning_System_for_Formal_Mathematics/image2.png
importance: 1
giscus_comments: true
link: https://arxiv.org/pdf/2601.14027
af_short_title: "Numina-Lean-Agent"
af_input: "Formal Statement"
af_output: "Formal Proof"
af_agents: [orchestrator, formal_prover, nlp_judge, subagent]
af_tools: [lean4_mcp, theorem_search, blueprint_tool]
af_tool_notes:
  lean4_mcp: "Lean-LSP-MCP provides semantic awareness (proof goals, file diagnostics), code execution (compile snippets, parallel strategy evaluation at single nodes), and theorem retrieval from local projects"
  theorem_search: "LeanDex performs semantic natural-language search over Lean v4.26.0 packages including Mathlib and FLT"
  blueprint_tool: "Blueprint Generation decomposes long-horizon tasks into a DAG of verifiable subgoals; revised dynamically based on Lean compilation feedback in a recursive loop"
af_agent_notes:
  orchestrator: "General coding agent (Claude Code) autonomously selects and invokes MCP tools to drive the overall proof search"
  formal_prover: "Agent writes Lean 4 code, compiles it, and iteratively repairs errors using diagnostics from Lean-LSP-MCP"
  nlp_judge: "Informal Prover subsystem: a Generator produces informal solutions and a Verifier checks correctness; a solution requires 3 independent passing verdicts in up to 20 iterations"
  subagent: "For lengthy proof trajectories, specific lemmas are isolated and assigned to independent subagents to avoid context-length limitations"
---

The input is lean4 formal statement. The goal is to prove the theorem.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Numina_Lean_Agent_An_Open_and_General_Agentic_Reasoning_System_for_Formal_Mathematics/image1.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

## Method

The framework utilizes a general coding agent (Claude Code) integrated with a modular toolset accessed via the Model Context Protocol (MCP), collectively named Numina-Lean-MCP. The system functions autonomously by selecting and invoking the following specialized tools to complete formal reasoning tasks:

*   **Lean-LSP-MCP**: A bridge between the language model and the Lean kernel via the Language Server Protocol. It provides tools across three dimensions:
    *   *Semantic Awareness*: Tools for querying proof goals and file structures (e.g., file outlines, diagnostic messages) directly from the compilation environment.
    *   *Code Execution*: Tools for compiling isolated code snippets and executing parallel strategy evaluations at single proof nodes.
    *   *Theorem Retrieval*: Tools for extracting definitions from local projects and searching the standard library.
*   **LeanDex**: A semantic search tool compatible with Lean v4.26.0. It interprets natural language queries to retrieve theorems and definitions across multiple packages, including Mathlib and FLT.
*   **Informal Prover**: An iterative two-model system consisting of a Generator and a Verifier. The Generator produces informal solutions which the Verifier assesses. If errors are identified, the Generator refines the solution based on the Verifier's feedback. This loop continues until acceptance or until a limit of $$20$$ iterations is reached. A solution is only accepted if the Verifier judges it correct in three independent passes.
*   **Discussion Partner**: A module that allows the primary agent to query other language models during the formalization process. It is used to generate alternative reasoning paths or strategy suggestions when encountering proof bottlenecks.
*   **Blueprint Generation**: An explicit planning layer that decomposes long-horizon formalization tasks into verifiable subgoals, represented as a directed acyclic graph. This step is recursive and coupled with the formalization loop; compilation feedback from Lean is used to revise the blueprint dynamically.
*   **Subagent Mechanism**: For lengthy proof search trajectories, specific lemmas are isolated and assigned to subagents. These subagents generate informal hints and conduct the corresponding formalization independently to mitigate context-length limitations.

## Experiments

The system was evaluated on the Putnam 2025 benchmark using the formal statements provided by Seed-Prover 1.5. All agent operations were executed sequentially, and internet access was disabled to prevent online retrieval of solutions.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Numina_Lean_Agent_An_Open_and_General_Agentic_Reasoning_System_for_Formal_Mathematics/image3.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Numina_Lean_Agent_An_Open_and_General_Agentic_Reasoning_System_for_Formal_Mathematics/image4.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>


The framework solved $$12$$ out of $$12$$ problems on the benchmark. By default, problems were allocated a computational budget of 50 USD. Problem A5 was allocated 1000 USD due to longer search trajectories, and problem B6 was allocated 300 USD.

#### Time spend

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Numina_Lean_Agent_An_Open_and_General_Agentic_Reasoning_System_for_Formal_Mathematics/image5.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>


####  Code length

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Numina_Lean_Agent_An_Open_and_General_Agentic_Reasoning_System_for_Formal_Mathematics/image6.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



An ablation study on problem B4 compared the Informal Prover's iterative refinement strategy against an independent sampling strategy. Holding the total number of API calls constant, the iterative refinement approach completed the formal proof in $$5$$ rounds, whereas the independent sampling approach failed to complete the proof within $$10$$ rounds.

## Formalizing Brascamp-Lieb with Numina-Lean-Agent

To demonstrate the system's capabilities on large-scale, novel mathematical reasoning, the authors conducted a case study formalizing the main theorem of the *Effective Brascamp–Lieb Inequalities*.

### How They Formalize
The formalization process relies heavily on a **plan–formalize–refine workflow** and human-AI collaboration:
*   The system creates a "blueprint"—an explicit planning artifact containing required definitions, a curated list of intermediate lemmas, and a directed acyclic graph (DAG) of dependencies. A higher-level reasoning model decomposes the proof, while Claude Code translates these steps into Lean.
*   **Human-AI Cooperation:** The formalization was conducted interactively. A mathematician and a Lean formalization expert collaborated with the agent by providing hints and modifying the initial blueprint to guide the overarching proof strategy.
*   **Adaptive Decomposition:** While formalizing, the agent dynamically introduced its own intermediate lemmas that were finer-grained than the initial human-provided blueprint to manage complex arguments.

### How They Evaluate Correctness
The system moves beyond traditional one-shot proving by using the formal environment as a ground-truth evaluator to actively correct mathematical reasoning:
*   **Recursive Compilation Feedback:** The agent continuously compiles its code in Lean. Feedback from the compiler (e.g., failed typeclass searches, mismatched interfaces) acts as a concrete signal to iteratively revise the blueprint, strengthen assumptions, or rephrase statements.
*   **Self-Correction of Statements:** Unlike traditional provers that attempt to prove a fixed statement or its negation, Numina-Lean-Agent actively evaluates the validity of the statements themselves. If it detects that a statement is mathematically incorrect or underspecified during the proof process, it can autonomously revise the formal statement (e.g., identifying and adding a missing degenerate-case assumption, such as handling a dimension-0 base space).

### Performance and Limitations
*   **Throughput and Autonomy:** In less than two weeks of intermittent collaboration, the human-AI team successfully produced over **8,000 lines of Lean code**. During this process, the agent autonomously introduced approximately **70 new definitions, lemmas, and theorems**, demonstrating its ability to participate in sustained formalization efforts.
*   **Limitations in Code Quality (Verbosity):** While functionally correct, the agent-generated proofs often lack formal elegance. Complete lemma proofs generated from scratch tend to be verbose, heavily reliant on low-level tactic scripts, and lack the structured abstraction expected in community libraries like Mathlib.
*   **Limitations with Type-Level Constraints:** The system occasionally failed on implicit type-level issues (e.g., conversions between `Real` and `NNReal`). Because these constraints are rarely explicit in informal mathematics, the agent struggled to resolve them without human intervention to adjust the workflow and make the definitions more "type-friendly."
