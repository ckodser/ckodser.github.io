---
layout: page
title: MerLean An Agentic Framework for Autoformalization in Quantum Computation
description: A bidirectional framework that extracts mathematical statements from LaTeX, formalizes them into Lean 4 code, and translates the verified code back into natural language.
categories: [autoformalization]
img: assets/img/MerLean_An_Agentic_Framework_for_Autoformalization_in_Quantum_Computation/image1.png
importance: 1
giscus_comments: true
link: https://arxiv.org/pdf/2602.16554
af_short_title: "MerLean"
af_input: "NLP Document"
af_output: "Formal Statement + Formal Proof"
af_agents: [formal_prover]
af_tools: [lean4_mcp, theorem_search]
af_tool_notes:
  lean4_mcp: "lean-lsp-mcp provides lean_goal to inspect proof states and lean_hover_info for type signatures; compilation errors are fed directly back to the agent for correction in the iterative compile-fix loop"
  theorem_search: "leansearch and loogle query Mathlib lemmas during formalization; also used to find definitions when the agent autonomously introduces auxiliary lemmas not present in the original paper"
af_agent_notes:
  formal_prover: "Single LLM agent in a multi-turn compile-fix loop: extracts statements from LaTeX, generates Lean 4 code, compiles it, and feeds compiler errors back for correction; also autonomously introduces auxiliary lemmas as needed"
---



## Method

MerLean is a bidirectional framework composed of two pipelines: autoformalization, which translates mathematical research papers from LaTeX into verified Lean 4 libraries built on Mathlib, and autoinformalization, which converts the formal code back into human-readable LaTeX. The framework utilizes a large language model agent to perform multi-turn interactions.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/MerLean_An_Agentic_Framework_for_Autoformalization_in_Quantum_Computation/image2.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



**Autoformalization Pipeline**

The autoformalization process follows four stages:
*   **Statement Extraction**: The agent extracts mathematical statements (definitions, theorems, lemmas, propositions, corollaries, remarks) from a LaTeX source file into a structured JSON representation. Each entry contains a unique identifier, the natural language mathematical content, explicit dependencies, and proof sketches.
*   **Iterative Formalization**: The agent enters a compile-fix loop for each extracted statement. It generates Lean 4 code, writes it to the library structure, and compiles it. Compilation errors are fed back to the agent for correction. The agent uses tools provided via `lean-lsp-mcp` (a Model Context Protocol server), such as `lean_goal` to inspect proof states, `lean_hover_info` for type signatures, and `leansearch` or `loogle` to query Mathlib lemmas.
*   **Faithfulness Checking**: After a successful compilation, the system verifies whether the compiled code matches the original mathematical meaning to prevent type-checking trivialities. If the semantic meaning is preserved, the system proceeds to the next statement.
*   **Axiom Handling**: For statements relying on mathematical results not yet available in Mathlib, MerLean implements explicit `axiom` declarations. If formalization fails after a set number of attempts, the framework converts blocking subgoals into axioms, producing a partial formalization.

**Autoinformalization Pipeline**

The decoder phase converts the verified Lean 4 library back into LaTeX. The agent that performed the formalization translates each declaration into natural language without access to the original paper's content. This pipeline constructs a dependency graph and outputs an interactive blueprint via `leanblueprint` alongside a standalone narrative file. Unverified assumptions (`axiom` declarations) are highlighted to indicate the boundaries of the formalization.

## Experiments

MerLean was evaluated on three theoretical quantum computing papers:

*   **Paper A: Balanced Product Codes**: Evaluates quantum codes constructed from tensor products and fiber bundles of chain complexes, utilizing homological algebra, tensor product of complexes, and spectral expansion.
*   **Paper B: Fault-Tolerant Quantum Computation**: Evaluates stabilizer codes, fault-tolerant protocols, transversal gates, and gauging graphs.
*   **Paper C: Quantum Topology**: An unpublished manuscript evaluating algebraic and group-theoretic properties of maps on quantum computational systems.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/MerLean_An_Agentic_Framework_for_Autoformalization_in_Quantum_Computation/image3.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



Across the three papers, the system formalized 114 statements into 2,050 Lean declarations in under 42 hours of wall-clock time. Paper A required explicit axioms for 9.1% of its statements due to missing Mathlib machinery (e.g., spectral sequences and Künneth isomorphisms for $$\mathbb{F}_2$$-chain complexes). The formalization process showed that theorems required the highest average processing time (39m 41s) and compile attempts (22.4), while remarks required the least (10m 34s and 7.1 attempts).

<div class="col-sm mt-3 mt-md-0">
    {% include figure.liquid path='assets/img/MerLean_An_Agentic_Framework_for_Autoformalization_in_Quantum_Computation/image4.png' class="img-fluid rounded z-depth-1" %}
</div>



The distribution of compile attempts was right-skewed. Most statements resolved within 1 to 10 attempts, while a subset required over 20 iterations. Compile-fix loops exceeding 20 attempts typically involved dependent type arithmetic (e.g., proving $$i - 1 + 1 = i$$ at the type level), missing lemmas, or tactic timeouts that necessitated proof restructuring.

During the process, the agent autonomously generated auxiliary lemmas not stated in the original papers to bridge logical steps. Examples include:
*   `edgeBoundary_card_eq_edgeCount`: Connected geometric expansion definitions to algebraic adjacency counts.

*   `pauliPair_anticommuting_ct_satisfied`: Algebraically verified that anticommuting spacetime faults cancel out disjointly.


Axiom declarations were used where the underlying mathematics were missing from Mathlib. Specific gaps identified included:
*   **Künneth Formula**: The isomorphism for chain complexes over $$\mathbb{F}_2$$:

$$
H_n(C \otimes D) \cong \bigoplus_{p+q=n} H_p(C) \otimes H_q(D)
$$

*   **Tensor-Homology Commutativity**: The isomorphism $$H_q(V \otimes C) \cong V \otimes H_q(C)$$ for a flat module $$V$$.
*   **Spectral Sequences**: The machinery for computing the homology of total complexes via spectral sequences to relate the $$E^2$$ page to total homology.
