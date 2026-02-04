---
layout: page
title: Top-down induction of decision trees- rigorous guarantees and inherent limitations
description: greedily learn a decision tree based on the most inflouential variables in all leaves.
categories: [Summary, ActiveLearning]
img: assets/img/Top_down_induction_of_decision_trees_rigorous_guarantees_and_inherent_limitations/img.png
importance: 1
giscus_comments: true
link: https://arxiv.org/abs/1911.07375
---

### Notations and Definitions

**Bare Decision Tree**: $$ T^\circ $$ is a bare decision tree which means it has unlabeled leaves).

**influence**: $$\text{Inf}_{i}(f)$$ is the influence of variable $$x_i$$ on $$f$$, defined as:

$$\text{Inf}_{i}(f) := \text{Pr}_{x \sim \{0,1\}^n}[f(x) \ne f(x^{\oplus i})]$$

with $$x$$ drawn uniformly at random and $$x^{\oplus i}$$ denoting $$x$$ with its $$i$$-th coordinate flipped.

**Total Influence**:
The total influence of a function $$f: \{0,1\}^n \rightarrow \{\pm1\}$$, denoted $$\text{Inf}(f)$$, is defined as:

$$\text{Inf}(f) = \sum_{i=1}^n \text{Inf}_{i}(f)$$

**error of bare tree**: $$\text{error}(T^{\circ}, f)$$ is the error of bare tree $$T^{\circ}$$ on function $$f$$, where we labeled leaves such that the error is minimized.

**error of function and $$\pm 1$$**: $$\text{error}(f, \pm 1)$$ is the error of $$f$$ with respect to $$+1$$ or $$-1$$ whichever best matches $$f$$ and gives it a low error.


---

### Method: **Top-Down Decision Tree Construction (BuildTopDownDT)**

The paper proposes and analyzes a heuristic for constructing decision trees for Boolean functions using a top-down approach with rigorous performance bounds. The method, named **BuildTopDownDT**, uses the variable *influence* as the splitting criterion.

---

### Key Steps in the Heuristic

1. **Initialization:**
   - Start with an empty decision tree $$ T^\circ $$.

2. **Scoring:**
   - For each current leaf $$ \ell $$, calculate the influence of variables in the sub-function $$ f_\ell $$ represented by that leaf.
     - The most influential variable at leaf $$ \ell $$ is denoted $$ x_i(\ell) $$, where $$ \mathrm{Inf}_{i}(f_{\ell}) \geq \mathrm{Inf}_j(f_{\ell}) $$ for all $$ j $$.
     - Assign a score to each leaf:

$$\text{score}(\ell) = \Pr_{x \sim \{0,1\}^n}[x \text{ reaches } \ell] \cdot \mathrm{Inf}_{i(\ell)}(f_{\ell}) = 2^{-\lvert \ell \rvert} \cdot \mathrm{Inf}_{i(\ell)}(f_{\ell}),$$

where $$\lvert \ell \rvert$$ is the depth of leaf $$ \ell $$.

3. **Splitting:**
   - Identify the leaf $$ \ell^* $$ with the highest score and split the tree at this leaf using the variable $$ x_{i(\ell^*)} $$.

4. **Stopping Criterion:**
   - Repeat the scoring and splitting process until the $$ f $$-completion of $$ T^\circ $$ is an $$\varepsilon$$-approximation of $$ f $$, where the error is bounded by $$ \varepsilon $$. $$ f $$-completion means assigning the best label to each leaf of $$T^\circ$$ such that it is best matched by $$ f $$.

---

#### Lower Bounds:
- For any error parameter $$ \varepsilon \in (0, \frac{1}{2}) $$, there exists a function $$ f $$ with decision tree size $$ s \leq 2^{\tilde{O}(\sqrt{n})} $$ such that the heuristic produces a decision tree of size:

$$s^{\Omega\left(\log \tilde{s}\right)}.$$


#### Upper Bounds:
**Theorem 3 (Upper bound for approximate representation)**
For every $$f$$ with decision tree size $$s$$ and every $$\epsilon \in (0, \frac{1}{2})$$, the heuristic constructs an approximate decision tree of size at most $$s^{O(\log(s/\epsilon) \log(1/\epsilon))}$$.

**Proof:**

The proof of this theorem relies on tracking a "cost" metric of the bare tree $$T^{\circ}$$ being built by the above algorithm. The heuristic terminates when the $$f$$-completion of $$T^{\circ}$$ is an $$\epsilon$$-approximation of $$f$$.


**1. Definition and Properties of "Cost"**
The cost of a bare tree $$T^{\circ}$$ relative to a function $$f: \{0,1\}^n \rightarrow \{\pm1\}$$ is defined as:

$$\text{cost}_f(T^{\circ}) = \sum_{\text{leaf } \ell \in T^{\circ}} 2^{-\\lvert \ell \\rvert} \cdot \text{Inf}(f_\ell)$$

where $$\\lvert \ell \\rvert$$ is the depth of leaf $$\ell$$ and $$f_\ell$$
is the restriction of $$f$$ by the path leading to $$\ell$$.

Lemma 5.1 states the following properties of the cost:
First $$\text{error}(T^{\circ}, f) \le \text{cost}_f(T^{\circ})$$. This means if the cost drops below $$\epsilon$$, the heuristic can terminate.

Second when a leaf $$\ell$$ in $$T^{\circ}$$ is replaced by a query to variable $$x_i$$,
resulting in a new bare tree $$(T^{\circ})'$$, the cost decreases by the score of the leaf:
$$\text{cost}_{f}((T^{\circ})') = \text{cost}_{f}(T^{\circ}) - 2^{-\\lvert \ell \\rvert} \cdot \text{Inf}_{i}(f_{\ell})$$.
The score of a leaf $$\ell$$ is defined as $$2^{-\\lvert \ell \\rvert} \cdot \text{Inf}_{i(\ell)}(f_\ell)$$,
where $$x_{i(\ell)}$$ is the most influential variable of $$f_{\ell}$$.

**2. Lower Bounds on the Score of the Leaf Selected**
The heuristic splits the leaf with the highest score. The proof uses two lower bounds on this score.

Lemma 5.2 states that at step $$j$$, the algorithm selects a leaf $$\ell^*$$ with score at least
$$\frac{\epsilon}{(j+1)\log(s)}$$. This is derived from the fact that if the completion is not an
$$\epsilon$$-approximation, there must be a leaf $$\ell$$ with
$$2^{-\\lvert \ell \\rvert} \cdot \text{error}(f_{\ell}, \pm 1) > \frac{\epsilon}{j+1}$$.
Using the relationship $$\text{Var}(g) \ge \text{error}(g, \pm 1)$$
and [Paper: Every decision tree has an influential variable](https://arxiv.org/abs/cs/0508071) ($$\max_{i} \text{Inf}_{i}(f) \ge \frac{\text{Var}(f)}{\log s}$$ ),
it follows that $$2^{-\\lvert \ell \\rvert} \cdot \text{Inf}_{i}(f_{\ell}) > \frac{\epsilon}{(j+1)\log(s)}$$ for some variable $$x_i$$.
Since the heuristic picks the leaf with the maximum score, the selected leaf's score is at least this value.

Lemma 5.4 provides a second lower bound, useful when the cost is large. If at step $$j$$, $$\text{cost}_f(T^{\circ}) \ge \epsilon \log(4s/\epsilon)$$, the selected leaf $$\ell^*$$ has score at least $$\frac{\text{cost}_f(T^{\circ})}{(j+1)\log(4s/\epsilon)\log(s)}$$. This lemma uses Lemma 5.3, which bounds the total influence of a size-$$s$$ decision tree: $$\text{Inf}(f) \le \text{Var}(f) \log(4s/\text{Var}(f))$$.

**3. Proof of Theorem 3**
Let $$C_j$$ be the cost after $$j$$ steps. The size of the resulting tree is $$j+1$$ if the algorithm terminates at step $$j$$. The algorithm terminates when $$C_j \le \epsilon$$. The analysis proceeds in two phases:

**Phase 1:** Reduce the cost until it is below $$\epsilon \log(4s/\epsilon)$$.
While $$C_j > \epsilon \log(4s/\epsilon)$$, the heuristic selects a leaf with score at least $$\frac{C_j}{(j+1)\log(4s/\epsilon)\log(s)}$$ (from Lemma 5.4).
From Lemma 5.1, $$C_{j+1} \le C_j - \frac{C_j}{(j+1)\log(4s/\epsilon)\log(s)} = C_j \left(1 - \frac{1}{(j+1)\log(4s/\epsilon)\log(s)}\right)$$.
After $$k$$ steps,

$$C_k \le C_0 \prod_{j=1}^k \left(1 - \frac{1}{j\log(4s/\epsilon)\log(s)}\right) \le C_0 \exp\left(-\sum_{j=1}^k \frac{1}{j\log(4s/\epsilon)\log(s)}\right)$$

Using $$\sum_{j=1}^k \frac{1}{j} \approx \log k$$,

$$C_k \le C_0 \exp\left(-\frac{\log k}{\log(4s/\epsilon)\log(s)}\right)$$

Since $$C_0 = \text{Inf}(f) \le \log s$$, setting $$k = s^{\log(4s/\epsilon)\log(1/\epsilon)}$$ ensures $$C_k \le \epsilon \log(4s/\epsilon)$$.

**Phase 2:** Reduce the cost from below $$\epsilon \log(4s/\epsilon)$$ to $$\epsilon$$.
Once $$C_j \le \epsilon \log(4s/\epsilon)$$, the heuristic selects a leaf with score at least $$\frac{\epsilon}{(j+1)\log s}$$ (from Lemma 5.2).
$$C_{j+1} \le C_j - \frac{\epsilon}{(j+1)\log s}$$.
For $$m > k$$, $$C_k - C_m \ge \sum_{j=k+1}^m \frac{\epsilon}{(j+1)\log s} \ge \frac{\epsilon}{\log s}(\log m - \log k)$$.
To ensure $$C_m \le \epsilon$$, we need $$C_k - \epsilon \ge \frac{\epsilon}{\log s}(\log m - \log k)$$. Setting $$\log m = \frac{\log s}{\epsilon} (C_k - \epsilon) + \log k$$.
Using $$C_k \le \epsilon \log(4s/\epsilon)$$ and the value of $$k$$ from Phase 1, $$m \le s^{2\log(4s/\epsilon)\log(1/\epsilon)}$$.

The total number of steps is at most $$m$$, so the size of the decision tree is at most $$m+1$$, which is $$s^{O(\log(s/\epsilon) \log(1/\epsilon))}$$.

Thus, for any function $$f$$ with decision tree size $$s$$ and error parameter $$\epsilon \in (0, \frac{1}{2})$$, the heuristic constructs an approximate decision tree of size at most $$s^{O(\log(s/\epsilon) \log(1/\epsilon))}$$.
