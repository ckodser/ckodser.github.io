---
layout: page
title: M2F Automated Formalization of Mathematical Literature at Scale
description: A two-stage framework for automated, project-scale formalization of mathematical literature into buildable Lean projects using verifier-certified refinement.
categories: [autoformalization]
img: assets/img/M2F_Automated_Formalization_of_Mathematical_Literature_at_Scale/image2.png
importance: 1
giscus_comments: true
link: https://arxiv.org/pdf/2602.17016
---

They use Human Domain Expert Audit to check the correctness of formalized statements. They make the task easier for the human checker by "Provenance-Linking". The auditor is shown the original textbook text side-by-side with the Lean code, making it easy to verify that nothing was lost or altered in translation.

# Method

M2F translates a long-form source document $$\mathcal{D}$$ (e.g., a LaTeX textbook or paper) into a Lean project $$\mathcal{P}$$ that compiles end-to-end under a fixed Lean environment $$\mathcal{E}$$. The fixed environment $$\mathcal{E}$$ consists of a specific Lean toolchain version and a pinned dependency revision.

The system interacts with the Lean toolchain through a file-level verification oracle:

$$ \text{VerifyFile}_{\mathcal{E}}(\mathcal{P}, f) \to (ok, \Delta_f) $$

where $$\Delta_f$$ is a finite multiset of diagnostics annotated with source ranges in the file $$f$$, and $$ok$$ indicates that the file elaborates successfully with zero error-level diagnostics.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/M2F_Automated_Formalization_of_Mathematical_Literature_at_Scale/image1.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



The framework operates in two stages, both governed by a verifier-certified accept/revert refinement loop. Bounded edits are proposed and committed if and only if the Lean toolchain feedback confirms a strict improvement according to the stage's specific objective.

**Stage 1: Statement Compilation**
The input document $$\mathcal{D}$$ is normalized into an ordered sequence of atomic blocks. The system maps these blocks to a Lean project $$\mathcal{P}_1$$ that elaborates end-to-end under $$\mathcal{E}$$ while allowing proof placeholders (e.g., `sorry`). For each block, an initial Lean declaration skeleton is inserted. If the file fails to compile, the system proposes localized patches conditioned on the error diagnostics. A patch is accepted if it strictly reduces the number of error-level diagnostics in the affected scope.

**Stage 2: Proof Repair**
Starting from $$\mathcal{P}_1$$, the system reduces the number of remaining proof holes to output the final project $$\mathcal{P}_2$$. This stage operates under matched statements: statement signatures are frozen, and edits are restricted to proofs and optional local helpers that do not modify existing signatures. For each proof placeholder, the system iterates a planner and prover to propose candidate patches. A proposed proof patch is accepted if it strictly reduces the total count of proof holes in the file while maintaining zero error-level compilation diagnostics.

# Experiments

M2F was evaluated on three long-form corpora and one external benchmark:
*   *Real Analysis*: 36 sections (312 pages) from Lebl's textbook.
*   *Convex Analysis*: 15 sections (140 pages) from Rockafellar's textbook.
*   *Paper*: 6 sections (27 pages) of research paper exposition.
*   *FATE-H*: 100 problems from a formal algebra benchmark.

**End-to-End Buildability and Statement Compilation**
Running the pipeline end-to-end on the 479 pages of long-form sources produced a Lean artifact consisting of 241 files, 4,116 declarations, and 153,853 lines of Lean code that builds successfully under the fixed environment $$\mathcal{E}$$.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/M2F_Automated_Formalization_of_Mathematical_Literature_at_Scale/image3.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



Stage 1 statement compilation achieved 100% statement compile coverage (SCC) across all textbook and paper sources. The average repair rounds (ARR) per block remained below 0.5 across all three sources, indicating that the majority of generated statements elaborated immediately or required zero patch attempts after initial generation.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/M2F_Automated_Formalization_of_Mathematical_Literature_at_Scale/image4.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



**Proof Repair under Matched Statements**
Stage 2 proof repair was evaluated under matched statements, where the statement layer generated in Stage 1 was held fixed and manually audited for faithfulness to the source text. The system successfully closed 100% of the audited proof holes on the three long-form corpora while preserving project-level elaboration.

Ablation studies on fixed dataset slices demonstrated the impact of different context constraints during repair. Removing structured goal/context conditioning (diagnostics-only) or disabling plan revision (no replanning) reduced the proof success rate (PSR), particularly on the research paper corpus where implicit dependencies are more frequent.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/M2F_Automated_Formalization_of_Mathematical_Literature_at_Scale/image5.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



On the FATE-H benchmark, where statements already elaborate in Lean, Stage 2 was evaluated in isolation. The system achieved a 96% proof success rate fully automatically. Providing a reproducible light-supervision condition—a mapping of 31 fully-qualified Lean declaration names with one-sentence natural language descriptions, without formal proof scripts—resulted in a 97% success rate.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/M2F_Automated_Formalization_of_Mathematical_Literature_at_Scale/image6.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
