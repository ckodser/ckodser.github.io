---
layout: page
title: Hilbert Recursively Building Formal Proofs with Informal Reasoning
description: A multi-agent framework that orchestrates general-purpose reasoning models and specialized prover models to recursively decompose and solve formal mathematical theorems.
categories: [autoformalizer]
img: assets/img/Hilbert_Recursively_Building_Formal_Proofs_with_Informal_Reasoning/image8.png
importance: 1
giscus_comments: true
link: https://arxiv.org/pdf/2509.22819
af_short_title: "HILBERT"
af_input: "Formal Statement"
af_output: "Formal Proof"
af_agents: [formal_prover, nlp_prover, break_to_lemma,subgoal_extractor, proof_assembler]
af_tools: [lean_mcp, mathlib_search]
af_datasets: [MiniF2F, PutnamBench]
af_tool_notes:
  lean_mcp: "The Kimina Lean Server running Lean 4. It acts as the formal verification loop, checking the syntactic and mathematical correctness of theorem statements, proof sketches, and formal proofs, and providing detailed error messages to guide the error_corrector. It has a concurrency mechanism built around Python's asyncio library that orchestrates parallel requests across the framework's multiple steps to optimize runtime efficiency."
  mathlib_search: "A semantic search engine built with sentence transformers and FAISS indexing. It retrieves the most relevant theorems and tactics from Mathlib by computing cosine similarity against informal theorem descriptions."
af_agent_notes:
  formal_prover: "A specialized prover LLM (e.g., DeepSeek-V2-7B or Goedel-Prover-V2 32B) that attempts to generate direct formal proofs given a formal theorem statement or an extracted sub-goal. They also attempt to solve subgoals directly with General LLMs as shallow_solver agent. shallow_solver agent: If the formal_prover fails to close a specific sub-goal, this agent uses retrieved theorems and the general-purpose reasoner to write targeted short proofs for that isolated sub-problem."
  nlp_prover: "A general-purpose reasoning LLM that generates step-by-step informal natural language proofs, and creates a Lean 4 proof sketch that decomposes complex reasoning into logical subgoals with 'sorry' placeholders. Analyzes compilation errors returned by the lean_verifier and iteratively refines incorrect proofs, fixes syntax errors in extracted subgoals, or revises flawed proof sketches based on compiler feedback."
  break_to_lemma: "A general-purpose reasoning LLM that generates step-by-step informal natural language proofs, and creates a Lean 4 proof sketch that decomposes complex reasoning into logical subgoals with 'sorry' placeholders. Analyzes compilation errors returned by the lean_verifier and iteratively refines incorrect proofs, fixes syntax errors in extracted subgoals, or revises flawed proof sketches based on compiler feedback. Same agent as nlp prover. There is only one agent that does both."
  subgoal_extractor: "Extracts the 'have' statements from the generated proof sketch, converting them into independent, isolated theorem statements with 'sorry' proofs and relevant contextual hypotheses."
  proof_assembler: "After subgoals are resolved, this agent replaces the 'sorry' placeholders in the proof sketch with calls to the proven subgoal theorems, assembling them back together into a complete proof for the main target theorem."
af_datasets_notes:
  MiniF2F: "HILBERT system achieved a 99.2% pass rate."
  PutnamBench: " solving 462 problems (70.0%)."
---

## Method

HILBERT is a multi-agent system that connects informal mathematical reasoning with formal verification. It applies recursive subgoal decomposition to divide complex theorems into simpler subgoals. The system coordinates four components:

*   **Reasoner**: A general-purpose large language model (LLM) (e.g., Gemini 2.5 Pro, gpt-oss-120b) used to write informal proofs, generate proof sketches in Lean 4, and occasionally write formal proofs.
*   **Prover**: A specialized LLM (e.g., DeepSeek-Prover-V2-7B, Goedel-Prover-V2-32B) optimized for writing formal proofs given a formal theorem statement.
*   **Verifier**: A formal language verifier (Kimina Lean Server with Lean v4.15.0 and Mathlib v4.15.0) used to check the syntactic and mathematical correctness of theorem statements and proofs.
*   **Retriever**: A semantic search engine utilizing sentence transformers and FAISS indexing to fetch relevant theorems from the Mathlib library.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Hilbert_Recursively_Building_Formal_Proofs_with_Informal_Reasoning/image1.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



Given a formal theorem statement in Lean 4, the system first attempts a direct proof using the Prover. The Prover generates $$K_{\text{initial proof}} = 4$$ candidate proofs. These are checked by the Verifier. If any proof is valid, it is returned. If all direct attempts fail, the system employs the Reasoner to execute the subgoal decomposition algorithm.

### Subgoal Decomposition

The subgoal decomposition process breaks the problem into subproblems and assembles a proof strategy.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Hilbert_Recursively_Building_Formal_Proofs_with_Informal_Reasoning/image2.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



1.  **Theorem Retrieval**: The Reasoner generates $$s = 5$$ search queries related to the formal statement. The Retriever fetches the top $$m = 5$$ most semantically similar theorems and tactics from Mathlib per query. The Reasoner filters these results to retain only relevant theorems.
2.  **Formal Proof Sketch Generation**: The Reasoner writes a detailed informal proof using the retrieved theorems. Using this as context, the Reasoner generates a Lean 4 proof sketch, breaking the problem into subproblems represented as `have` statements. Subgoals are initially filled with the `sorry` placeholder keyword. The Verifier checks the sketch. In case of errors, Verifier feedback is used to correct the sketch. The system allows up to $$K_{\text{sketch attempts}} = 4$$ attempts per theorem.
3.  **Subgoal Extraction**: The Reasoner converts the `have` statements from the proof sketch into independent theorem statements, carrying over relevant context from the original problem and preceding subgoals. The Verifier checks the syntax of each extracted theorem, and errors are fed back to the Reasoner for correction.
4.  **Sketch Assembly from Subgoals**: The Reasoner receives the extracted subgoal theorem statements and the validated proof sketch. It produces an assembled proof by replacing each `sorry` placeholder with calls to the corresponding extracted subgoal theorem. The Verifier checks both the assembled proof and the subgoal statements together to confirm structural validity.

### Subgoal Verification

Once the proof structure is validated, the system verifies the mathematical correctness and provability of the individual subgoals.

1.  **Prover Attempts**: The Prover attempts to solve each subgoal directly, generating $$K_{\text{formal proof}} = 4$$ candidate proofs. Valid proofs are accepted.
2.  **Correctness Verification**: For subgoals the Prover cannot solve, the Reasoner evaluates whether the subgoal is mathematically correct, properly formulated, and provable. If identified as incorrect or unprovable, the subgoal is flagged, and the system returns to the proof sketch generation step, incorporating the identified issues as feedback.
3.  **Shallow Solve**: For subgoals that pass correctness verification but fail Prover attempts, the Reasoner attempts a "shallow solve". After retrieving relevant Mathlib theorems, the Reasoner writes a short formal proof. It refines the proof using Verifier feedback for up to $$K_{\text{proof correction}} = 6$$ passes. The step terminates early if an incorrect proof exceeds $$K_{\text{max shallow solve length}} = 30$$ lines. The shallow solve process repeats for up to $$K_{\text{informal passes}} = 6$$ attempts.
4.  **Recursive Decomposition and Proof Assembly**: Subgoals remaining unproven after the previous steps undergo recursive subgoal decomposition. Each subgoal is subdivided until it is proven or the process reaches the maximum recursion depth $$D$$. If all subgoals are proven, the system concatenates the subgoal proofs with the assembled proof outline to yield the complete proof. If any subgoals remain unsolved, the current proof attempt fails, prompting a restart of the decomposition process for the parent theorem.

## Experiments

The system is evaluated on two formal mathematical reasoning benchmarks: MiniF2F and PutnamBench. In all experiments, the maximum recursion depth is set to $$D = 5$$.

### Main Results

**MiniF2F**: The test split of MiniF2F contains 244 high-school mathematics competition problems. Performance is evaluated using combinations of formal Provers (DeepSeek-Prover-V2-7B, Goedel-Prover-V2-32B) and informal Reasoners (Gemini 2.5 Flash, Gemini 2.5 Pro, gpt-oss-120b).

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Hilbert_Recursively_Building_Formal_Proofs_with_Informal_Reasoning/image3.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



The configuration combining Gemini 2.5 Pro with Goedel-Prover-V2-32B achieves a 99.2% pass rate, failing on two problems. Combining DeepSeek-Prover-V2-7B with Gemini 2.5 Pro yields 98.4%, while pairing it with Gemini 2.5 Flash yields 96.7%. Using the open-weights model gpt-oss-120b alongside Goedel-Prover-V2-32B results in a 90.8% pass rate.

**PutnamBench**: This benchmark consists of 660 undergraduate-level problems from the William Lowell Putnam Mathematical Competition. The system was tested using the Goedel-Prover-V2-32B Prover.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Hilbert_Recursively_Building_Formal_Proofs_with_Informal_Reasoning/image4.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



The configuration using Gemini 2.5 Pro solves 462 out of 660 problems (70.0% pass rate). The configuration using gpt-oss-120b solves 88 out of 660 problems (13.3%).

### Scaling Behavior with Inference-Time Compute

The system adapts inference-time compute across multiple interconnected stages based on problem difficulty. Figure 3 plots the pass rate on MiniF2F as a function of the number of calls to the Reasoner and the total number of LLM calls (Reasoner + Prover).

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Hilbert_Recursively_Building_Formal_Proofs_with_Informal_Reasoning/image5.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



Pass rates scale continuously with the number of calls. The Gemini 2.5 Pro with Goedel Prover configuration reaches its peak pass rate utilizing a maximum of 4.5K Reasoner calls and 11.3K total LLM calls per sample. Models with weaker Reasoners (Gemini 2.5 Flash) require higher inference budgets to reach their respective peak pass rates. Token consumption increases in tandem with pass rate improvements; on MiniF2F, the most challenging problems consume up to 27.0M tokens for the Gemini 2.5 Pro + DeepSeek-Prover-V2 configuration.

### Ablation Studies

**Performance vs Depth**: The effect of the recursive depth $$D$$ on subgoal decomposition is evaluated on MiniF2F using Gemini 2.5 Pro and Goedel-Prover-V2-32B. A baseline of $$D=0$$ (standalone Prover at pass@4) achieves a 75% pass rate.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Hilbert_Recursively_Building_Formal_Proofs_with_Informal_Reasoning/image6.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



Performance increases monotonically with depth. The full system reaches a 98.36% pass rate at $$D=2$$ and 98.7% at $$D=3$$. An ablated version with the shallow solve mechanism disabled ($$K_{\text{informal passes}} = 0$$) requires a greater recursion depth to reach comparable performance.

**Retrieval Ablation**: The impact of the Retriever component is tested by comparing the full system against a variant without retrieval.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Hilbert_Recursively_Building_Formal_Proofs_with_Informal_Reasoning/image7.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



Including retrieval increases the pass rate and decreases inference-time compute utilization. For the DeepSeek-Prover-V2-7B configuration, retrieval increases the pass rate from 97.1% to 98.4%, reduces average Reasoner calls per problem from 426 to 420, and lowers average Reasoner tokens from 2.1M to 1.9M. For the Goedel-Prover-V2-32B configuration, retrieval increases the pass rate from 97.9% to 99.2%, while decreasing average Reasoner calls from 862 to 548 and average Reasoner tokens from 4.0M to 2.3M.
