---
layout: page
title: Towards a Common Framework for Autoformalization
description: A unified conceptual framework defining autoformalization across interactive theorem proving, logic programming, planning, and knowledge representation.
categories: [autoformalization]
img: assets/img/Towards_a_Common_Framework_for_Autoformalization/image1.png
importance: 2
giscus_comments: true
link: https://arxiv.org/pdf/2509.09810
---

## Method

The proposed framework models autoformalization as the transformation of natural or semi-formal text into formal representations. The core process is formalized by the following definition:

Formalization from informal language $$L_i$$ to formal reasoning language $$L_f$$ with respect to a semantic equivalence criterion $$E$$ is the transformation of an expression in a domain-specific subset of $$L_i$$ into a well-formed and valid expression in $$L_f$$ that is semantically equivalent according to $$E$$. Autoformalization is formalization performed automatically by a computing system.

The definition consists of four primary parameters:

*   **Informal language ($$L_i$$)**: A collection of meaningful expressions, such as grammatically well-formed natural language texts or semi-formal mathematical proofs. The framework targets domain-specific subsets of $$L_i$$ that share a common conceptual framework, rather than attempting to formalize all possible expressions.
*   **Formal reasoning language ($$L_f$$)**: An enumerable set of expressions specified by a grammar or formation rules. $$L_f$$ requires a formal semantics that assigns unambiguous meaning to each well-formed expression and an accompanying reasoning apparatus (e.g., inference or transformation rules) to derive new expressions while preserving semantic properties. Examples include languages of interactive theorem provers (e.g., Lean, Isabelle), fully formal logics (e.g., First-Order Logic, Linear Temporal Logic), declarative programming languages (e.g., Prolog, Answer Set Programming), planning languages (e.g., PDDL), and knowledge representation formalisms (e.g., OWL, RDF).
*   **Semantic equivalence criterion ($$E$$)**: A theoretical standard specifying the conditions under which the formalized expression in $$L_f$$ preserves the intended and relevant meaning of the informal input from $$L_i$$.
*   **Validation criterion ($$V$$)**: A computable approximation of $$E$$. Because $$E$$ relies on the inherently ambiguous semantics of informal languages, $$V$$ provides a practical, automated or semi-automated mechanism for verifying that a given pair of informal and formal expressions satisfies the required semantic equivalence.

## Experiments

The framework is applied to five distinct domain settings to map their specific inputs, formal targets, and validation criteria.

### Formalization of Mathematics with Interactive Theorem Provers
The input $$L_i$$ consists of natural mathematical language, specifically mathematical problem descriptions. The target language $$L_f$$ is Isar, the structured proof language of the Isabelle/HOL interactive theorem prover.

For an informal input:
*Prove that there is no function $$f$$ from the set of non-negative integers into itself such that $$f(f(n)) = n + 1987$$ for every $$n$$.*

The generated formalization in Isabelle/HOL is:
```isabelle
theorem
fixes f :: "nat \<Rightarrow> nat"
assumes "\<forall> n. f (f n) = n + 1987"
shows False
```
The semantic equivalence criterion $$E$$ requires that all mathematical assumptions and constraints are preserved in the formal theorem statement. The validation criteria $$V$$ applied in this setting include BLEU scores to measure surface-level similarity against ground-truth manual formalizations, alongside manual human evaluation to confirm semantic accuracy.

### First-Order Logic
The input $$L_i$$ comprises natural language questions regarding real-world objects and shapes. The target formalism $$L_f$$ is Prover9, utilizing first-order logic syntax.

For an informal input specifying that all squares have four sides and all four-sided things are shapes, the system constructs a set of predicates and formal premises:

$$ \forall x(\text{Square}(x) \rightarrow \text{FourSided}(x)) $$

$$ \forall x(\text{FourSided}(x) \rightarrow \text{Shape}(x)) $$

The system evaluates the conclusion:

$$ \forall x(\text{Square}(x) \rightarrow \text{Shape}(x)) $$

The criterion $$E$$ requires the logical formulas to capture relevant object properties without introducing spurious parameters. The validation criterion $$V$$ is measured by executing the reasoning engine over the formal representation and comparing the derived Boolean answer to a ground-truth label.

### Logic Programming
The input $$L_i$$ involves natural language descriptions of strategic interactions, specifically bimatrix games (e.g., Battle of the Sexes). The target language $$L_f$$ consists of Prolog programs, with reasoning executed via the SWI-Prolog solver.

The output maps player preferences and actions to a payoff matrix utilizing domain-specific and domain-independent predicates:
```prolog
payoffBOS(opera, opera, 2, 1).
payoffBOS(football, football, 1, 2).
payoffBOS(opera, football, 0, 0).
payoffBOS(football, opera, 0, 0).
```
The equivalence criterion $$E$$ requires the strict formalization of game rules and utility parameters. Validation $$V$$ is completely automated by querying the generated Prolog program for all possible action combinations and comparing the resulting payoff outputs to a ground-truth matrix.

### Planning
The input $$L_i$$ relies on natural language action descriptions supplemented with allowed predicate symbols. The target language $$L_f$$ is the Planning Domain Definition Language (PDDL).

For an informal instruction to fly an airplane between locations, the output formalizes the preconditions and effects into a labeled transition system:
```lisp
(:action FLY-AIRPLANE
 :parameters (?airplane - airplane ?loc-from - airport ?loc-to - airport)
 :precondition (at ?airplane ?loc-from)
 :effect (and(not(at ?airplane ?loc-from)) (at ?airplane ?loc-to)) )
```
The semantic equivalence criterion $$E$$ tests for domain equivalence, capturing both action behavior and logical consequence. Validation $$V$$ utilizes a heuristic domain equivalence test: valid plans generated in a reconstructed domain are cross-validated against the original domain using a plan validation tool. If validation succeeds, semantic behavior is deemed equivalent:

$$ \text{Semantics}(L_f') \approx \text{Semantics}(L_f) $$

### Knowledge Representation
The input $$L_i$$ maps concise declarative natural language sentences to Web Ontology Language (OWL) axioms expressed in Functional Syntax.

For the sentence *Anna and Lana are each other's sisters*, the output generates respective TBox and ABox assertions:
```text
Declaration(ObjectProperty(:has_sister))
Declaration(NamedIndividual(:Anna))
Declaration(NamedIndividual(:Lana))
ObjPropAssert(:has_sister :Anna :Lana)
ObjPropAssert(:has_sister :Lana :Anna)
```
The semantic equivalence criterion $$E$$ requires that all relational information is captured by the ontology structure. Validation $$V$$ relies primarily on manual verification by ontology engineers. This is supplemented by automated consistency checking and entailment verification utilizing formal ontology reasoners to identify unintended consequences.
