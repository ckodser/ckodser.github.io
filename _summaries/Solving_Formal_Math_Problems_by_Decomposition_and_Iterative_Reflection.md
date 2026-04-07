---
layout: page
title: Solving Formal Math Problems by Decomposition and Iterative Reflection
description: An agent-based framework that orchestrates interaction between a general-purpose LLM and the Lean 4 environment via reflective decomposition and iterative proof repair.
categories: [autoformalization]
img: assets/img/Solving_Formal_Math_Problems_by_Decomposition_and_Iterative_Reflection/image6.png
importance: 1
giscus_comments: true
link: https://arxiv.org/pdf/2507.15225
af_short_title: "Delta Prover"
af_input: "Formal Statement + NLP Statement"
af_output: "Formal Proof"
af_agents: [NLP_prover, break_to_lemma, formal_prover]
af_tools: [lean4_mcp, custom_lean4_dsl, theorem_search]
af_datasets: [MiniF2F]
af_dataset_notes:
    miniF2F: "244 math problems collected from mathematics competitions and the MATH dataset. A more challenging subset consisting strictly of all International Mathematical Olympiad (IMO) problems within the miniF2F-test benchmark."
af_tool_notes:
    lean4_mcp: "Serves as the absolute ground truth, actively compiling and executing LLM-generated code. When a proof attempt fails, the kernel outputs diagnostic information including the specific error location and current tactic state, guiding the Iterative Proof Repair agent toward a correct solution."
    custom_lean4_dsl: "Built using Lean 4's metaprogramming, this tool provides specialized syntax for high-level proof sketching and goal management. It allows agents to introduce hypotheses, define arbitrary expressions, and isolate sub-problem contexts without needing immediate proofs. Native Lean 4 is optimized for low-level tactics rather than managing unproven, interconnected sub-goals."
    theorem_search: "Intervenes when the Iterative Proof Repair agent struggles with the vast Mathlib4 library. If the Lean 4 kernel flags an unknown or incorrectly named identifier, this tool searches for and retrieves correct theorem names, definitions, and signatures, injecting retrieved context back into the prompt."
af_agent_notes:
    NLP_prover: "Creates a step-by-step informal proof plan based on the original problem statements. By receiving both the formal and natural language statements, it formulates a high-level strategic outline that bridges human reasoning and formal logic. This informal plan serves as a direct blueprint for the subsequent formal decomposition phase. "
    break_to_lemma: "Utilizes a custom Domain-Specific Language (DSL) to translate the informal proof plan into a formal proof sketch. It breaks down complex, intractable theorems into manageable sub-problems. If downstream proving attempts fail, this agent exhibits reflective capabilities by analyzing the failed sub-problems and regenerating a revised, alternative decomposition sketch."
    proof_assembler: "There is an other agent that does the oposite and stick these part to gather: proof_consolidator acts as the final assembly mechanism once all individual sub-problems have been successfully verified. It utilizes the custom DSL to systematically replace placeholders in the formal sketch with the corresponding successful sub-proofs, integrating isolated steps into a single, cohesive, and formally verified Lean 4 proof for the original theorem."
    formal_prover: "Operating in a tight feedback loop, this agent takes formal statements or decomposed sub-problems and actively attempts to write Lean 4 proof code. When initial proof attempts fail validation, it analyzes diagnostic error messages and retrieved tactics to progressively correct and refine its code. This iterative cycle continues until the agent successfully satisfies the verification kernel or exhausts its iteration limits."
---

## Method

Delta Prover integrates a general-purpose Large Language Model (LLM) with the Lean 4 proof environment. The framework operates through an iterative loop consisting of two primary components: Iterative Proof Repair and Reflective Decomposition.

Let $$S$$ denote a formal statement, $$s$$ its corresponding natural language version, $$P$$ a formal proof, $$p$$ an informal proof plan, and $$D$$ a formal proof sketch expressed in a Domain-Specific Language (DSL).

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Solving_Formal_Math_Problems_by_Decomposition_and_Iterative_Reflection/image1.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



### Iterative Proof Repair

The LLM is prompted with the formal statement $$S$$ to generate an initial formal proof candidate $$P^0$$. The prompt includes guidelines on:
*   **Formatting Conventions**: Instructions on syntax following tactics (e.g., `rcases`, `cases`).
*   **Effective Tactics**: Doc-strings and examples for Mathlib tactics such as `linarith`, `ring`, and `omega`.
*   **Lean 4 Specification**: Instructions to strictly output Lean 4 code instead of Lean 3.

If the statement-proof pair $$(S, P^0)$$ validates against the Lean 4 kernel, the process terminates. If a proof attempt $$P^i$$ fails validation, the Lean 4 kernel returns an error message. For the next iteration, the prompt is augmented with:
*   The incorrect proof $$P^i$$.
*   The tactic state and error message from the Lean 4 kernel.
*   Retrieved theorems and definitions based on errored names or incorrect identifiers.

The LLM generates a revised proof $$P^{i+1}$$. This cycle repeats until a valid proof is found or a predetermined maximum number of iterations is reached.

### Reflective Decomposition

For proofs that require multiple steps, the framework breaks down the original problem into sub-problems.

1.  **Initial Formal Sketch Construction**: The LLM generates an informal proof plan $$p$$ from $$(S, s)$$. The LLM then generates a formal proof sketch $$D$$ using a custom DSL. The prompt includes DSL format guidelines and highlights common auto-formalization pitfalls.
2.  **Sub-problem Extraction and Solving**: The DSL parses the draft $$D$$ and extracts formal statements for the required sub-proofs ($$S_1, \dots, S_n$$). Valid sub-problems are passed to the Iterative Proof Repair loop.
3.  **Iterative Decomposition Repair**: If any sub-problems are not solved by the Iterative Proof Repair loop, the failures are logged. The LLM is prompted to regenerate the proof sketch $$D$$ with a revised decomposition strategy, using the list of unsolved sub-problems as feedback.

### Overall Framework

Delta Prover initially attempts a direct solution using Iterative Proof Repair. If unsuccessful, it initiates Reflective Decomposition. If Reflective Decomposition yields a list of solved sub-problems, the framework performs Automatic Proof Consolidation. During consolidation, the derived sub-proofs $$P_i$$ are substituted back into the DSL-based sketch, and concluding commands are appended to produce the complete formal proof $$P$$ for the original statement $$S$$.

### Decomposition via Extended Syntax

The custom Domain-Specific Language (DSL) is built on Lean 4's metaprogramming facilities using a monad layer, `PlayM`, built upon `TacticM`. It manages intermediate proof states and converts them into valid Lean 4 proof scripts.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Solving_Formal_Math_Problems_by_Decomposition_and_Iterative_Reflection/image2.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



The DSL provides four tactics:
*   **`Suppose`**: Introduces new hypotheses into the proof context.
*   **`Define`**: Introduces arbitrary Lean 4 expressions and infers their types.
*   **`ShowBy`**: Creates subgoals and interfaces with Mathlib tactics. It records generated proofs for later assembly.
*   **`Conclude`**: Consolidates proofs by leveraging recorded steps, dependency graphs, and Lean 4's delaborator to emit a coherent Lean 4 proof.

## Experiments

### Basic Experiment Setup

*   **Model**: Gemini 2.5 Pro 05-06 with sampling temperature set to $$1$$.
*   **Benchmarks**:
    *   **miniF2F-test**: 244 problems from mathematics competitions and the MATH dataset translated into Lean 4.
    *   **miniF2F-test-IMO**: A subset consisting of all IMO problems within miniF2F-test.

### Benchmark Performance

Delta Prover is evaluated against baseline provers on the miniF2F-test benchmark. Sample budgets are determined by recording the number of API calls used for a successful attempt and taking the maximum across all solved problems.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Solving_Formal_Math_Problems_by_Decomposition_and_Iterative_Reflection/image3.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



Delta Prover achieves an accuracy of 95.9% on miniF2F-test using a sample budget of 16384 API calls. The test-time scaling properties are tracked by measuring the accuracy relative to the available sample budget.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Solving_Formal_Math_Problems_by_Decomposition_and_Iterative_Reflection/image4.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



### Ablation Studies

**Effect of Iterative Proof Repair**
The impact of Iterative Proof Repair is tested using only proof construction (without Reflective Decomposition). The total budget is fixed at 1024 API calls. The experiment varies the number of iterative repairs per round ($$n$$) and the number of rounds ($$m$$).

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Solving_Formal_Math_Problems_by_Decomposition_and_Iterative_Reflection/image5.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



Results indicate that accuracy increases as the number of repairs $$n$$ increases for a fixed total budget $$m \times n$$. When the number of repairs is constrained to $$n = 1$$, the process is equivalent to a Best-of-N (BoN) sampling strategy. The repair-enabled configurations yield higher accuracy than the BoN configuration at equivalent computational budgets.

**Effect of Reflective Decomposition**
The role of Reflective Decomposition is evaluated using IMO 2019 Problem 1 from the miniF2F-test set. Two strategies are compared:
1.  **Baseline**: Pure iterative proof correction.
2.  **Delta Prover**: Iterative proof correction combined with Reflective Decomposition.

The baseline approach did not find a solution after 1024 API calls. Using Reflective Decomposition, the problem was separated into 83 sub-problems during the initial decomposition round. Each sub-problem required an average of 4 API calls to resolve. The complete problem was solved using approximately $$83 \times 4 = 332$$ API calls.
