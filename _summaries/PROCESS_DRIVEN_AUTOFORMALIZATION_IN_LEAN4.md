---
layout: page
title: Process-Driven Autoformalization in Lean 4
description: This paper introduces the Process-Driven Autoformalization (PDA) framework, which leverages process-level feedback from the Lean 4 compiler to iteratively improve the autoformalization of natural language mathematics.
categories: [autoformalization]
img: assets/img/2406_01940v2_pdf/image2.png
importance: 1
giscus_comments: true
link: https://arxiv.org/pdf/2406.01940
---

## Dataset

They introduce FormL4. They translate back MathLib 4 theorems/proofs to Natrual language and manually check their correctness. They did not check the correctness of NLP proofs.

## How they translate formals to informal?
Use Gemini-Pro-1.5 for translation. Filter out theorems that needs hard lemmas. The process is as follows:

1. Translate the Statement: Convert the formal theorem statement into a natural-language math problem without mentioning any Lean 4 functions.
2. Explain the Proof (Reasoning Buffer): Explain the meaning of each line/tactic in the formal proof based on the definitions of the lemmas used. This acts as a "scratchpad" or reasoning buffer for the model to understand the logic.
3. Construct the Final Proof: Write a fluent, step-by-step mathematical proof in natural language, entirely independent of the formal syntax and without verbatim mentions of Lean 4 code.
4. Manual check by Lean4 experts.

## Training

They trained a model using their dataset.

## Inference

The model is given theorem statement and proof in NL. Goal: translate statement and proof to Lean4.

1. The system takes the prompt and generates multiple candidate formalizations. Each candidate includes both the formal Lean 4 theorem statement and the formal Lean 4 proof tactics using the fine-tuned Mistral-v0.3-7B model.
2. Then they extract the Lean4 from output
3. Instead of compiling all of candidates, the system evaluates the generated candidates to predict which one is most likely to compile successfullyusing Process-Supervised Verifier (PSV).
4. The best candidate according to PSV is send to lean4 compiler; If pass they conculde the autoformalization is correct.

## Validation/results

They take 60 random autoformalization samples and manually check the correctness. They find that 25% of the things that pass their system are still wrong.
