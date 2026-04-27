---
layout: page
title: Seed-Prover 1.5 Mastering Undergraduate-Level Theorem Proving via Learning from Experience
description: Documentation of the training methodologies and experimental scaling results of the Seed-Prover 1.5 formal theorem proving model.
categories: [autoformalizer]
img: assets/img/Seed_Prover_1_5_Mastering_Undergraduate_Level_Theorem_Proving_via_Learning_from_Experience/image10.png
importance: 1
giscus_comments: true
link: https://arxiv.org/pdf/2512.17260
af_short_title: "Seed-Prover 1.5"
af_input: "Formal Statement"
af_output: "Formal Proof"
af_agents: [nlp_prover, break_to_lemma, formal_prover]
af_tools: [lean_mcp, mathlib_search, code_execution]
af_datasets: [PutnamBench, FATE, CombiBench, IMO, Erdős]
af_tool_notes:
  lean_mcp: "A REPL-based Python interface for Lean. It compiles individual lemmas sequentially instead of requiring a whole proof, storing the statement header and proven lemmas in the running context, and returns structured feedback to the model."
  mathlib_search: "An embedding-based semantic retrieval tool (using sentence transformers and FAISS) calibrated to Mathlib v4.22.0. It identifies relevant theorems, lemmas, or definitions based on semantic similarity to a query."
  code_execution: "An interface that allows the agent to generate and run Python scripts, enabling numerical experiments, calculations, and computational checks during the proving trajectory."
af_agent_notes:
  natural_language_prover: "An LLM optimized for generating rigorous, lemma-style natural language proofs. It provides the initial high-level strategic reasoning to guide the formalization process."
  break_to_lemma: "A translation agent trained via Rubric RL (VAPO). It acts as a hierarchical problem decomposer by converting the natural language proofs into lemma-style Lean sketches, outlining auxiliary lemmas with 'sorry' placeholders."
  formal_prover: "A tool-integrated LLM trained via large-scale Agentic Reinforcement Learning. It iteratively attempts to prove or disprove each unsolved lemma within the sketch using tools. If a lemma is verified, it caches it as an axiom to reduce context overhead; if a lemma is disproved, it triggers the sketch model to refine the plan."
af_datasets_notes:
  PutnamBench: "A dataset of 660 undergraduate-level problems from the Putnam Mathematical Competition. Seed-Prover 1.5 achieved an 87.9% solve rate (580 problems). The 2025 Putnam Competition problem set. Seed-Prover 1.5 successfully solved 11 out of 12 problems within a 9-hour window."
  FATE: "A benchmark suite featuring FATE-H (100 honors/graduate-level problems) and FATE-X (100 PhD-level qualifying exam problems). The system solved 80% of FATE-H and 33% of FATE-X."
  CombiBench: "A benchmark centered on combinatorial problems often involving novel concepts. Seed-Prover 1.5 achieved a 48% solve rate, though the authors noted significant formalization issues in the dataset."
  IMO: "The 2025 International Mathematical Olympiad problem set. The system solved 5 out of the 6 problems using a moderate compute budget (10 H20-days/problem)."
  Erdős: "A subset of open mathematical problems/conjectures from the Erdős problem sets. The model solved 15 problems, though the authors note these specific problems were mathematically simpler or simplified due to mis-formalization."
---


## Method

The system consists of a formal theorem proving model trained via agentic reinforcement learning and a hierarchical test-time scaling workflow.

### Agentic Prover
The prover uses an incremental strategy to construct formal proofs step by step through multiple tool invocations. Once a lemma is compiled successfully, it is cached in memory and reused in subsequent reasoning steps, preventing the regeneration of verified code. The available tools include Lean verification, Mathlib search via embedding-based retrieval, and Python execution. During inference, generation terminates when the theorem is verified or when the interaction budget (64K maximum sequence length and a limit of 28 tool calls) is exhausted.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Seed_Prover_1_5_Mastering_Undergraduate_Level_Theorem_Proving_via_Learning_from_Experience/image1.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



### Post-training
The model is initialized using supervised fine-tuning (SFT) on synthetic data to learn tool invocation patterns in the Lean environment. Reinforcement learning (RL) optimization is implemented using VAPO. An outcome-based reward function is applied: the model receives a reward of $$1$$ if a proof is verified by the Lean compiler, and $$-1$$ otherwise. The proximal policy optimization objective is defined as:

$$
\mathcal{L}_{PPO}(\theta) = - \frac{1}{G} \sum_{i=1}^{G} \frac{1}{|o_i|} \sum_{t=1}^{|o_i|} \min \left( r_{i,t}(\theta) \hat{A}_{i,t}, \text{clip}\left(r_{i,t}(\theta), 1 - \varepsilon_{\text{low}}, 1 + \varepsilon_{\text{high}}\right) \hat{A}_{i,t} \right)
$$

where $$G$$ is the batch size, $$o_i$$ is the trajectory of the $$i$$-th sample, $$\hat{A}_{i,t}$$ is the estimated advantage at time step $$t$$, $$\varepsilon$$ is the clipping hyperparameter, and $$r_{i,t}(\theta)$$ is the probability ratio.

### Sketch Model
A sketch model synthesizes a lemma-style Lean sketch from a formal statement and its natural language proof. It decomposes the proposition into $$N$$ independent sub-goals. The model is trained using VAPO with a hybrid reward signal. The reward function $$R$$ requires the generation of at least three lemmas, structural correctness verified by Lean ($$S_{\text{FL}}$$), and semantic validity verified by an LLM-as-a-Judge ($$S_{\text{NL}}$$):

$$
R = \begin{cases} 1 & \text{if } N_{\text{lemmas}} \ge 3 \land S_{\text{FL}} \ge 0 \land S_{\text{NL}} \ge 0.7, \\ -1 & \text{otherwise}. \end{cases}
$$



### Test-Time Workflow
The system uses a hierarchical workflow coordinating three agents:
1. **Natural Language Prover:** Generates lemma-style natural language proofs.
2. **Sketch Model:** Converts natural language proofs into lemma-style Lean sketches.
3. **Agentic Lean Prover:** Verifies individual lemmas.

For each unsolved lemma, the Agentic Prover attempts verification under a compute budget. If unverified, recursive decomposition (natural language proof to Lean sketch) is performed until leaf nodes are proved or the maximum search depth is reached.

## Experiments

Evaluations were conducted using Lean v4.22.0 across multiple benchmarks: PutnamBench, FATE-H, FATE-X, CombiBench, IMO 2025, Putnam 2025, and a subset of Erdős problems.

### Scaling Behavior of Agentic Prover Training
During RL training, batch-level accuracy increases from 50% to nearly 90% after 1000 steps. The average number of function calls per trajectory decreases from 15 to 10, accompanied by a reduction in average sequence length from ~28k to ~17k tokens. The model adapts its search tool usage based on the dataset, averaging 10 search calls per trajectory on Fate-H and 1–2 on Putnam.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Seed_Prover_1_5_Mastering_Undergraduate_Level_Theorem_Proving_via_Learning_from_Experience/image2.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>


<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Seed_Prover_1_5_Mastering_Undergraduate_Level_Theorem_Proving_via_Learning_from_Experience/image3.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Seed_Prover_1_5_Mastering_Undergraduate_Level_Theorem_Proving_via_Learning_from_Experience/image4.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Seed_Prover_1_5_Mastering_Undergraduate_Level_Theorem_Proving_via_Learning_from_Experience/image5.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>


<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Seed_Prover_1_5_Mastering_Undergraduate_Level_Theorem_Proving_via_Learning_from_Experience/image6.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



### Test-Time Workflow Evaluation
On PutnamBench, test-time compute scaling (search width and search depth) yields a log-linear increase in the solve rate. The majority of problems are solved within the initial hours, with the distribution extending to the 53rd hour.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Seed_Prover_1_5_Mastering_Undergraduate_Level_Theorem_Proving_via_Learning_from_Experience/image7.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



The system solves 87.9% of PutnamBench, 80% of FATE-H, 33% of FATE-X, and 48% of CombiBench problems.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Seed_Prover_1_5_Mastering_Undergraduate_Level_Theorem_Proving_via_Learning_from_Experience/image8.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



On the IMO 2025 and Putnam 2025 competitions, maximum search depth was capped at 4. The model solved 11 out of 12 problems from Putnam 2025 within 9 hours, using a maximum compute budget of 40 H20-days per problem.
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Seed_Prover_1_5_Mastering_Undergraduate_Level_Theorem_Proving_via_Learning_from_Experience/image9.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
