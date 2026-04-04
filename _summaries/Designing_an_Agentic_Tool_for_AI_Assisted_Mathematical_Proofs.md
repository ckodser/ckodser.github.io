---
layout: page
title: Designing an Agentic Tool for AI-Assisted Mathematical Proofs
description: A five-layer orchestration architecture for AI-assisted mathematical proof development incorporating computational experimentation, adversarial review, and formal verification.
categories: [autoformalization]
img: assets/img/Designing_an_Agentic_Tool_for_AI_Assisted_Mathematical_Proofs/image1.png
importance: 1
giscus_comments: true
link: https://althofer.de/agentic_strategy_design_for_math_proofs.pdf
af_short_title: "Designing Agentic Tool (proposal)"
af_input: "NLP Statement"
af_output: "Formal Statement + Formal Proof"
af_agents: [orchestrator, computational_agent, synthesis_agent, adversarial_reviewer]
af_tools: [lean4_mcp, literature_search, code_execution]
af_tool_notes:
  lean4_mcp: "Formalization Bridge translates proof slices into Lean or Coq; compilation failures are extracted as minimal missing obligations (type mismatches, missing lemmas) and fed back into the adversarial review loop as blocking items"
  literature_search: "Two-pass semantic search: a pre-solve pass identifies prior art and likely techniques; a post-solve pass uses the generated proof structure to detect subsumption by existing results"
  code_execution: "Computational Agent writes and runs experimental code for numerical exploration and counterexample search, operating under a dedicated code-review loop before results inform proof strategy"
af_agent_notes:
  orchestrator: "Controls pipeline routing and human checkpoints based on a confidence score; maintains the Claim Ledger that requires every nontrivial statement to link to a specific evidence object"
  computational_agent: "Writes and optimizes experimental code for numerical exploration and counterexample search before a proof is attempted, to catch false conjectures early"
  synthesis_agent: "Constructs meta-prompted proof plans and executes them to produce LaTeX proofs; revises in response to adversarial feedback under a fixed change budget"
  adversarial_reviewer: "Scrutinizes proof drafts for logical gaps and proposes exact replacement text for the Synthesis Agent to accept or reject"
---

This is not a paper really. This is a paper plan. Like there is no experiment. But there is many experiment designes ready.


## Method

The system implements a five-layer pipeline coordinated by an orchestrator managing three specialized agent roles: the Computational Agent, the Synthesis Agent, and the Review Agent. All inter-layer hand-offs occur via versioned artifacts to provide a reproducible audit trail.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Designing_an_Agentic_Tool_for_AI_Assisted_Mathematical_Proofs/image1.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>


### Orchestrator and Confidence Calibration

The orchestrator controls pipeline routing, human checkpoints, and review loop termination based on a defined risk level $$\rho$$, a resource budget $$B$$, and a derived confidence score $$c \in [0, 1]$$.

The confidence score aggregates binary and graded signals from the verification processes. A baseline aggregation uses a logistic model:

$$
c = \sigma(w_0 + w_{int}s_{int} + w_{rev}s_{rev} + w_{exp}s_{exp} + w_{form}s_{form} + w_{lit}s_{lit} + w_{axm}s_{axm})
$$

The weights $$w$$ are calibrated on a held-out set of problems and recalibrated following toolchain updates. Until a stable empirical reliability curve is established, $$c$$ is truncated and human escalation remains the default policy.

### Layer Specifications

**Layer 1: Problem Understanding & Disambiguation**
This layer generates a versioned Interpretation Dossier. It standardizes the canonical statement and produces a definition lockfile to fix mathematical conventions. It also generates semantic unit tests to verify specific edge cases or boundary conditions that rule out common misinterpretations.

**Layer 2: Literature Search & Context**
Layer 2 executes a two-pass semantic search. The pre-solve pass identifies prior art and likely techniques to inform proof generation. The post-solve pass uses the structure of the generated proof to detect subsumption. Outputs are compiled into a Literature Dossier, containing a theorem dependency graph and claim coverage matrices.

**Layer 3: Computational Experimentation**
For problems involving numerical or finite objects, the Computational Agent writes and executes experimental code. This layer operates under a distinct code-review loop to ensure empirical reliability before data is used to inform proof strategy.

**Layer 4: Proof Generation & Adversarial Refinement**
Proof generation relies on a meta-prompted two-phase approach (planning followed by execution) executed by the Synthesis Agent.

The output undergoes an iterative adversarial review loop against the Review Agent. To enforce prioritization of critical logical gaps over stylistic differences, the loop operates under a fixed change budget (e.g., maximum 3 high-impact changes per iteration). The Review Agent provides specific replacement text for the Synthesis Agent to accept or reject.

A Formalization Bridge translates local proof slices into Lean or Coq. This bridge enforces statement-proof separation: the formal statement is generated or verified independently from the proof generation process. Formalization failures are extracted as minimal missing obligations (e.g., type mismatches, missing lemmas) and fed back into the review loop as blocking items.

**Layer 5: Post-Verification & Novelty**
The final layer checks the proof against the Interpretation Dossier and evaluates novelty using a conservative decision rule based on the Literature Dossier. It also extracts recurring formalization errors and prompt refinements into a pitfall registry for future runs.

### Agents

### 1. The Experimentalist (Computational Agent)
*   **Goal:** To run computational experiments before a proof is attempted, in order to guide the proof strategy and catch false conjectures early.
*   **Primary Responsibilities:** Write and optimize experimental code for numerical exploration, and search for counterexamples.
*   **Outputs:** Code, numerical results, visualizations, and proof sketches.
*   *(Detailed on Page 9, Section 6.1)*

### 2. The Architect (Synthesis Agent)
*   **Goal:** To construct the actual mathematical proofs and iteratively fix them based on feedback.
*   **Primary Responsibilities:** Create meta-prompted proof plans, execute those plans to produce formal LaTeX proofs, and revise the proofs in response to adversarial review feedback.
*   **Outputs:** Structured proof plans, complete LaTeX proofs, and revised proof versions.
*   *(Detailed on Page 10, Section 6.2)*

### 3. The Reviewer (Adversarial Agent)
*   **Goal:** To act as an adversary that finds logical flaws in the Architect's proof drafts and suggests exact fixes.
*   **Primary Responsibilities:** Scrutinize proofs for logical leaps and errors, and propose concrete replacement text ("hints") for the Synthesis Agent (or a human) to accept, reject, or modify.
*   **Outputs:** Structured reviews in LaTeX containing proposed corrections.
*   *(Detailed on Page 10, Section 6.3)*

### 4. The Orchestrator
*   **Goal:** To act as the overall "Coordination layer" that manages the workflow, enforces rules, and acts as a bridge between the AI agents and the human user.
*   **Primary Responsibilities:**
    *   Classify problems and determine which pipeline branches to activate.
    *   Manage human checkpoints (interpretation, strategy, final review).
    *   Track the exact proof state (which definitions are in scope, what is proven vs. assumed vs. cited) via the "Claim Ledger".
    *   Enforce termination criteria and "change budgets" for the review loops.
    *   Compile "Context Bundles" so agents only see the precise information they need.
*   *(Detailed on Page 10, Section 6.4)*


### Structured Proof Context Management

Proof state is maintained using a Claim Ledger that requires every nontrivial statement to link to a specific evidence object:

*   **Derivation:** Linked to specific lemmas/steps.
*   **Citation:** Linked to BibTeX key and location.
*   **Computation:** Linked to code hash and random seed.
*   **Formal:** Linked to a Lean/Coq theorem name.


Agent prompts are dynamically constructed as Context Bundles. The orchestrator compiles these bundles under a strict token budget $$T$$, prioritizing the definition lockfile and current goal $$G$$, followed by blocking review items, checked dependency theorem statements, and stylistic constraints.

## Experiments  (not done, only proposed)

The system is evaluated using a fixed, versioned benchmark suite and a structured reporting protocol.

### Benchmark Suite Design

The benchmark suite partitions problems into distinct difficulty tiers and types:
*   **Interpretation-stress:** Problems with multiple valid conventions where misinterpretation is common.
*   **Literature-heavy:** Problems likely solved in existing literature to test subsumption detection.
*   **Experiment-friendly:** Problems with finite objects or counterexamples.
*   **Formalization-friendly / Formalization-hostile:** Problems categorized by the density of required background formalization (e.g., algebraic fragments vs. heavy geometry).

### Evaluation Metrics

Outputs are evaluated across five primary axes: interpretation accuracy, logical soundness, meaningfulness, novelty, and reproducibility.

Resource utilization is tracked to measure system efficiency. Required metrics include wall-clock time, token usage per layer, review iteration counts, retrieval queries, experiment compute measured in CPU/GPU-hours, and required human intervention time at checkpoints.

### Ablations and Regression Testing

To quantify the marginal value and computational cost of each system component, controlled ablations are performed against the benchmark suite. Evaluated configurations include:
*   Full system pipeline
*   Removal of Layer 1 semantic unit tests
*   Removal of Layer 2 post-solve subsumption pass
*   Removal of Layer 3 computational experimentation
*   Removal of fixed change budgets in the Layer 4 review loop
*   Removal of the Claim Ledger evidence hard gate
*   Removal of the Formalization Bridge

Large cost increases measured during ablations are treated as design regressions unless accompanied by measurable gains in logical soundness or interpretation accuracy. Semantic unit tests and artifact validity checks are promoted to automated regression tests run upon any toolchain or model update.
