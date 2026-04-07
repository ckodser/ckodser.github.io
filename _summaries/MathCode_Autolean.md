---
layout: page
title: MathCode / AUTOLEAN
description: A terminal-based AI coding assistant with a built-in math formalization engine that converts natural language math problems into Lean 4 formal theorem statements and proofs.
categories: [autoformalization]
img: assets/img/MathCode_Autolean/banner.png
importance: 0.9
giscus_comments: true
link: https://github.com/math-ai-org/mathcode
af_short_title: "MathCode"
af_input: "NLP Statement"
af_output: "Formal Statement + Formal Proof"
af_agents: [planner, formal_statement, formal_prover, NLP_prover]
af_tools: [lean4_mcp, literature_search, file_system, anti_trivialization_guard]
af_statement_formalization_evaluation: "Two-layer check: (1) hardcoded anti-trivialization guard rejects statements reduced to True/False, (2) LLM-based semantic evaluator grades fidelity A-D against original NLP problem on 5-point checklist (objects, quantifiers, hypotheses, conclusions, multi-part coverage). Optional strict A+ recheck and double-check mode with cross-model agreement."
af_tool_notes:
  lean4_compiler: "Core verification tool invoked via lake env lean. Compiles generated Lean 4 files against a Mathlib-configured workspace. Provides structured error messages for repair loops. Ground-truth correctness oracle."
  literature_search: "Optional tool for Thinking and Coding agents via OpenRouter web search plugin. Queries internet for Mathlib documentation, theorem names, and mathematical references. Configurable search engine and max results."
  file_system: "Reads input JSON files from input directory, writes generated Lean files to output directory, maintains detailed per-iteration logs (thinking/coding/compiler stdout/stderr, evaluation payloads, metadata JSON)."
  anti_trivialization_guard: "Deterministic code-level policy check (not an LLM). Parses theorem header and rejects statements where the main proposition is trivially True or False. Enforces sorry in formalization-only mode and no sorry in require-no-sorry mode."

af_agent_notes:
  planner: "Phase 5.2. Runs only on iteration 1. Derives proof strategy, identifies exact Mathlib lemma names, flags coercion/typeclass pitfalls. Uses a potentially different thinking model (e.g., gpt-5.2 at xhigh reasoning effort) with optional web search. Outputs structured plain text, no Lean code."
  formal_statement: "Phase 5.3. Takes planning notes plus original JSON and generates a complete Lean 4 file. On repair iterations (2+), receives previous Lean file, compiler errors, and error memory of recurring failures. Uses coding-optimized model (e.g., gpt-5.2-codex). Outputs strict JSON with lean field."
  semantic_check: "Evaluates semantic fidelity after successful compilation. Uses separate LLM call (default gpt-5.2 at xhigh) with 5-point checklist: core objects/domains, quantifier structure, hypotheses, conclusions, multi-part coverage. Grades A-D; below threshold (default B) triggers retry with feedback."
  NLP_prover: "Separate script (prove_lean_formalizations_replan.py). Takes formalized Lean statement with sorry and generates proof plan. Uses planner model (default gpt-5.4). Replans after configurable number of failed proof attempts with latest failure report."
  proof_prover: "Takes Lean file with sorry placeholder and generates actual proof body. Preserves everything outside proof body. Rejects outputs containing sorry/admit or introducing new top-level declarations or axiom/constant/postulate. Multiple parallel attempts, each with own compile-repair loop."
---

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/MathCode_Autolean/main_image.svg' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

## Method

MathCode is a terminal-based AI coding assistant with a built-in math formalization engine called AUTOLEAN. Given a math problem in plain natural language (as a JSON file with a `uuid` and `problem` field), it automatically converts it into a Lean 4 formal theorem statement and optionally produces a formal proof. The system is a fixed pipeline (not a dynamic multi-agent orchestrator), where each stage acts as a distinct agent.

The core formalization pipeline proceeds as follows:

*   **Thinking/Planning Agent (Phase 5.2)**: Runs only on the first iteration. Analyzes the NLP problem, derives a proof strategy, identifies exact Mathlib lemma names likely to be needed, and flags coercion/typeclass pitfalls. Uses a thinking-optimized model with optional web search. Outputs structured planning notes without writing any Lean code.

*   **Formalizer/Coder Agent (Phase 5.3)**: Takes the planning notes and the original JSON problem to generate a complete Lean 4 file containing the formalized theorem statement (and optionally a proof). On repair iterations, it additionally receives the previous Lean file, compiler error output, and an error memory of recurring failures.

*   **Anti-Trivialization Guard**: A deterministic code-level check (not an LLM call) that parses the theorem header and rejects any statement where the main proposition is trivially `True` or `False`. This prevents the LLM from replacing the real problem with a vacuous statement that compiles easily.

*   **Lean 4 Compiler**: Executes `lake env lean` against the generated `.lean` file within a Mathlib-configured workspace. If compilation fails, errors are fed back to the Formalizer in a compile-repair loop (up to 6 iterations by default).

*   **Semantic Evaluator**: After successful compilation, a separate LLM grades the formalization's fidelity against the original NLP problem on a 5-point checklist (core objects/domains, quantifier structure, hypotheses, conclusions, multi-part coverage). Formalizations scoring below the threshold (default B) are rejected and retried with evaluator feedback.

For proof completion, two separate scripts extend the pipeline:

*   **Proof Planner**: Generates proof strategies for formalized statements. Replans after a configurable number of failed attempts, incorporating the latest failure report.

*   **Proof Prover**: Replaces `sorry` placeholders with actual proofs. Multiple independent attempts run in parallel, each with its own compile-repair loop. Rejects outputs that still contain `sorry`/`admit` or introduce unauthorized declarations.

The system supports multiple LLM backends (OpenRouter API, Codex Exec, Claude CLI), optional web search for mathematical references, and parallel workers across problems.

## Statement Fidelity Checking

Since MathCode produces the formal statement itself, it has two mechanisms to prevent trivialized or incorrect formalizations:

1.  **Anti-Trivialization Guard (Hardcoded Policy)**: Detects and rejects statements where the top-level proposition is literally `True` or `False`. Only catches the most blatant trivializations.

2.  **Semantic Evaluator (LLM-based Grading)**: Applies a detailed 5-point checklist to grade fidelity A-D. Grade D for trivialized/vacuous statements, C for missing major obligations, B for minor issues, A for fully faithful. An optional strict A+ recheck distinguishes exact matches from broadly faithful ones. A double-check mode can require cross-model agreement (e.g., both Gemini Flash and GPT-5.2 must assign grade A).
