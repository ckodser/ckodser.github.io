---
layout: page
title: Autoformalizer with Tool Feedback
description: A framework that improves autoformalization by integrating syntactic compiler feedback and semantic consistency checks during the generation process.
categories: [autoformalization]
img: assets/img/Autoformalizer_with_Tool_Feedback/image4.png
importance: 1
giscus_comments: true
link: https://arxiv.org/pdf/2510.06857
af_short_title: "ATF"
af_input: "NLP Statement"
af_output: "Formal Statement"
af_agents: [formalizer, semantic_check]
af_tools: [lean4_mcp]
af_datasets: [ProverBench, FormalMath-Lite, CombiBench]
af_statement_formalization_evaluation: "For the human evaluation, three domain experts independently review 100 randomly sampled instances from each benchmark, with the majority opinion serving as the final performance judgment."
af_tool_notes:
  lean4_mcp: "This tool evaluates the syntactic validity of the generated Lean 4 statements. It uses a pre-check to filter out obvious errors like missing libraries or unmatched parentheses, and then groups statements to efficiently acquire compilation feedback directly from the Lean 4 compiler. This feedback provides the Formalizer Agent with precise guidance for syntax corrections."
af_agent_notes:
  formalizer: "The core Autoformalizer model acts as the primary agent that translates the natural language mathematical problems into structured formal language. It operates iteratively during inference, actively generating statements, calling evaluation tools, and modifying its output based on the resulting error feedback."
  semantic_check: "This tool acts as an NLP-to-Formal-Language semantic check. It receives the informal problem alongside the generated formal statement and returns a consistency result with a concise explanation. To accurately identify subtle misalignments, it employs an ensemble vote method using multiple Large Language Models, confirming consistency only when the models give identical conclusions."
---

## Method

The Autoformalizer with Tool Feedback (ATF) incorporates syntactic and semantic consistency information as tools during the formalization process. The model adaptively refines generated formal statements based on feedback from these tools.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Autoformalizer_with_Tool_Feedback/image1.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



### Tool Design

The framework employs two distinct tools to evaluate the validity of formal statements:

**Syntax Check:** This tool processes formal statements and returns compilation feedback from the Lean 4 compiler. To reduce execution overhead, it utilizes a pre-check stage to filter out statements with obvious errors, such as missing libraries or unmatched parentheses. Subsequently, it uses a grouped execution method where statements are batched based on import libraries, concatenated into a single code file, and executed simultaneously.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Autoformalizer_with_Tool_Feedback/image2.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



**Consistency Check:** This tool evaluates semantic equivalence between the informal query and the generated formal statement. It relies on a multi-LLMs-as-judge approach using an ensemble vote. Consistency is only confirmed when both evaluating models return identical conclusions, which reduces the false positive rate when identifying minor inconsistencies.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Autoformalizer_with_Tool_Feedback/image3.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>


### Training Pipeline

The training process for ATF utilizes a subset of the NuminaMath-1.5 dataset and consists of three stages:

1. **Cold Start for Tool Integration:** The model is fine-tuned on synthetic multi-turn tool invocation trajectories. The data enforces specific execution rules: the syntax check must be invoked after any revision, the consistency check is only permitted after the syntax check passes, and the process stops when both checks pass.
2. **Expert Iteration:** The model generates formalization attempts on the remaining mathematical queries. Trajectories that result in successful formalization with fewer than 8 revision attempts are collected and merged with previous training data to further refine the model's formalization capabilities.
3. **Direct Preference Optimization (DPO):** To reduce ineffective revisions (e.g., repeating the same syntax error), DPO is applied. For each query, a trajectory with fewer revision attempts is selected as the positive sample ($$y_w$$), and one with more attempts is selected as the negative sample ($$y_l$$). The training uses a DPO loss combined with a negative log-likelihood (NLL) loss on the chosen trajectories:

$$
\mathcal{L} = -\mathbb{E} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right] - \alpha \mathbb{E} \left[ \log \pi_\theta(y_w|x) \right]
$$

where $$\pi_\theta$$ is the policy model, $$\pi_{\text{ref}}$$ is the reference model, $$\beta$$ is the temperature parameter, $$\alpha$$ is the weighting coefficient, and $$\sigma$$ represents the sigmoid function.

## Experiments

### Experimental Setup

Models were trained using full-parameter fine-tuning. Evaluations were conducted on three Automated Theorem Proving (ATP) datasets: FormalMath-Lite, ProverBench, and CombiBench. Metrics include Syntactic Validity (SC) and Semantic Consistency (CC). Generated statements were sampled 16 times per query to report Pass@1, Pass@8, and Pass@16 rates.

### Main Results

ATF was compared against baseline formalizer models across the three benchmarks. The evaluation indicates higher pass rates for both syntax and consistency metrics across all three datasets.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Autoformalizer_with_Tool_Feedback/image5.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



On the out-of-distribution CombiBench dataset, which features combinatorial mathematical problems, the ATF-32B model maintained a Pass@1 consistency score of $$65.38\%$$. Increased sampling rates (Pass@16) yielded consistency scores of $$100\%$$ on CombiBench and $$99.52\%$$ on FormalMath-Lite for the 32B model. The distilled 8B version of the model yielded a Pass@1 consistency of $$91.12\%$$ on FormalMath-Lite.

### Ablations

Ablation studies were conducted by systematically removing the consistency check or both tools entirely.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Autoformalizer_with_Tool_Feedback/image6.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



Removing tool guidance entirely results in a decrease in consistency check pass rates across all benchmarks. Including only the syntax check provides partial improvements, while combining both tools yields the highest semantic consistency. The staged training approach (Cold Start $$\rightarrow$$ Expert Iteration $$\rightarrow$$ DPO) shows cumulative pass rate increases at each phase.

### Scaling and Tool Analysis

Inference scaling properties were tested by extending the maximum allowed revision attempts and parallel sampling counts ($$k$$).

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Autoformalizer_with_Tool_Feedback/image7.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



Pass rates on consistency checks continue to scale as the number of revision attempts increases, despite the model being trained with a strict limit of fewer than 8 revisions. Parallel sampling further increases the overall pass rate.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Autoformalizer_with_Tool_Feedback/image8.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



Tool usage frequency varies depending on the dataset; combinatorial queries in CombiBench required more tool calls on average than queries in FormalMath-Lite. Analysis of revision efficiency indicates that the success rate of the consistency check decreases with each subsequent revision attempt, dropping from $$69.5\%$$ on the first attempt to $$8.8\%$$ on the eighth attempt.
