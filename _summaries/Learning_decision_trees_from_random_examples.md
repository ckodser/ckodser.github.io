---
layout: page
title: Learning decision trees from random examples
description: Decision tree learning By Finding Consistent Decision Trees
categories: [Summary, ActiveLearning]
img: assets/img/Learning_decision_trees_from_random_examples/img.png
importance: 1
giscus_comments: true
link: https://www.sciencedirect.com/science/article/pii/0890540189900011
---

This summary focuses exclusively on the technical aspects of the paper concerning learning decision trees, including definitions, notations, the main theorems, and their proofs.


### Definitions and Notations for Decision Trees

  * **Variables:** $$V_n = {v_1, ..., v_n}$$ is a set of $$n$$ Boolean variables.
  * **Input Domain:** $$X_n = {0,1}^n$$.
  * **Class of Decision Trees ($$T_n$$):** Recursively defined as follows:
      * A single root node labeled 0 or 1 is in $$T_n$$ (abbreviated as $$Q=0$$ or $$Q=1$$).
      * If $$Q_0, Q_1 \in T_n$$ and $$v \in V_n$$, then the binary tree with root labeled $$v$$, left subtree $$Q_0$$ (0-subtree), and right subtree $$Q_1$$ (1-subtree) is in $$T_n$$.
  * **Boolean Function Representation ($$f_Q$$):** A decision tree $$Q \in T_n$$ represents a Boolean function $$f_Q$$:
      * If $$Q=0$$, $$f_Q$$ is the constant function 0.
      * If $$Q=1$$, $$f_Q$$ is the constant function 1.
      * Else if $$v_i$$ is the label of the root of Q, $$Q_0$$ the 0-subtree, and $$Q_1$$ the 1-subtree, then for $$x=(a_1, ..., a_n) \in {0,1}^n$$, if $$a_i=0$$ then $$f_Q(x)=f_{Q_0}(x)$$, else $$f_Q(x)=f_{Q_1}(x)$$.
  * **Reduced Decision Tree:** A decision tree where each variable appears at most once in any path from the root to a leaf.
  * **Rank of a Decision Tree ($$r(Q)$$):** Defined recursively:
      * If $$Q=0$$ or $$Q=1$$, then $$r(Q)=0$$.
      * Else if $$r_0$$ is the rank of the 0-subtree of Q and $$r_1$$ is the rank of the 1-subtree, then $$r(Q) = \max(r_0, r_1)$$ if $$r_0 \ne r_1$$, and $$r(Q) = r_0+1 (=r_1+1)$$ otherwise.
  * $$T_n^r$$: The set of all decision trees in $$T_n$$ of rank at most $$r$$.
  * $$F_n^r$$: The set of Boolean functions on $$X_n$$ represented by trees in $$T_n^r$$.

-----

### Lemma 1

- Let $$k$$ be the number of nodes in a reduced decision tree over $$V_n$$ of rank $$r$$, where $$n \ge r \ge 1$$. Then $$2^{r+1}-1 \le k \le (2\sum_{i=0}^{r}\binom{n}{i})-1 < 2(\frac{en}{r})^r$$.
- If $$r=0$$ then $$|F_n^r|=2$$. Else if $$n \le r$$ then $$|F_n^r|=2^{2^n}$$, and if $$n > r$$ then $$|F_n^r| \le (8n)^{(\frac{en}{r})^r}$$.

**Proof of Lemma 1:**

(i) By induction, the smallest decision tree of rank $$r$$ is a complete binary tree of depth $$r$$, which has $$2^{r+1}-1$$ nodes. Thus, $$2^{r+1}-1 \le k$$.
Let $$L(n,r)$$ be the maximum number of leaves of any reduced decision tree over $$V_n$$ of rank $$r$$. From the definition of rank:
$$L(0,r)=1$$ for all $$r \ge 0$$.
$$L(n,0)=1$$ for all $$n \ge 0$$.
$$L(n,r)=L(n-1,r)+L(n-1,r-1)$$ for all $$n,r \ge 1$$, because the variable in the root of a reduced tree does not appear in its subtrees.
The solution for this recurrence for $$n \ge r$$ is $$L(n,r)=\sum_{i=0}^{r}\binom{n}{i}$$, which is bounded by $$(\frac{en}{r})^r$$ for $$n \ge r \ge 1$$. Since a binary tree has one less internal node than leaves, this yields the second and third inequalities for $$k$$.

(ii) If $$r=0$$, $$F_n^r$$ contains only constant functions, so $$|F_n^r|=2$$. If $$n \le r$$, $$T_n^r$$ includes every full binary decision tree of depth $$n$$, so $$F_n^r$$ includes all Boolean functions on $$X_n$$, and thus $$|F_n^r|=2^{2^n}$$. 
If $$n > r \ge 1$$, each function in $$F_n^r$$ is represented by a binary tree with at most $$k=(\frac{en}{r})^r$$ leaves. The number of distinct binary decision trees on $$n$$ variables with at most $$k$$ leaves is at most 

$$\sum_{i=1}^{k}\frac{2^{i}n^{i-1}}{2i-1}\binom{2i-1}{i}<(2n)^{k}\sum_{i=1}^{k}\binom{2k-1}{i}<(2n)^{k}2^{2k-1}<(8n)^{k}$$. 

Therefore, $$|F_n^r| \le (8n)^{(\frac{en}{r})^r}$$.

---

### Definitions for Finding Consistent Decision Trees

  * **Example:** A pair $$(x, f(x))$$ for a Boolean function $$f$$ on $$X_n$$. It is positive if $$f(x)=1$$, else negative.
  * **Rank of a Sample ($$r(S)$$):** The minimum rank of any decision tree consistent with $$S$$.
  * **Informative Variable:** A variable $$v$$ is informative on $$S$$ if we have at least one sample with $$x_v=0$$ and at least one with $$x_v=1$$. 

### Procedure FIND(S, r)

**Input:** A nonempty sample $$S$$ of some Boolean function on $$X_n$$ and an integer $$r \ge 0$$.

**Output:** A decision tree of rank at most $$r$$ consistent with $$S$$ if one exists, else "none".

1.  If all examples in $$S$$ are positive, return $$Q=1$$; if all are negative, return $$Q=0$$.
2.  If $$r=0$$, return "none".
3.  For each informative variable $$v \in V_n$$:
    1. Let $$Q_0^v = \text{FIND}(S_0^v, r-1)$$ and $$Q_1^v = \text{FIND}(S_1^v, r-1)$$.
    2. If both recursive calls succeed (neither $$Q_0^v=\text{none}$$ nor $$Q_1^v=\text{none}$$), return the decision tree with root labeled $$v$$, 0-subtree $$Q_0^v$$, and 1-subtree $$Q_1^v$$.
    3. If one recursive call succeeds but the other does not:
       1. Reexecute the unsuccessful call with rank bound $$r$$ instead of $$r-1$$ (e.g., if $$Q_1^v$$ is a tree but $$Q_0^v=\text{none}$$, let $$Q_0^v = \text{FIND}(S_0^v, r)$$).
       2. If the reexecuted call succeeds, let $$Q$$ be the decision tree with root labeled $$v$$, 0-subtree $$Q_0^v$$, and 1-subtree $$Q_1^v$$, else let $$Q=\text{"none"}$$.
       3. Return $$Q$$.
4.  Return "none".

-----

### Lemma 3 (Time of FIND)

For any nonempty sample $$S$$ of a function on $$X_n$$ and $$r \ge 0$$, the time of FIND$$(S,r)$$ is $$O(|S|(n+1)^{2r})$$.

**Proof of Lemma 3:**
Let $$T(i,r)$$ be the max time for FIND$$(S,r)$$ when $$S$$ is a sample on $$X_n$$ with $$1 \le |S| \le m$$ and at most $$i$$ variables are informative.
If $$i=0$$, $$T(i,r)$$ is $$O(1)$$ (since $$|S|=1$$). If $$r=0$$, $$T(i,r)$$ is $$O(m)$$.
For $$r \ge 1$$, steps 1 and 3 (determining informative variables) take $$O(mn)$$ time. Each of the two recursive calls in step 3A takes at most $$T(i-1, r-1)$$ time, as $$v$$ is no longer informative. These calls are made at most $$i$$ times, totaling $$2iT(i-1, r-1)$$ for step 3A. Step 3C.1 makes at most one recursive call to $$FIND(S_0^v, r)$$ or $$FIND(S_1^v, r)$$, taking at most $$T(i-1, r)$$ time.
Therefore, for $$r \ge 1$$: $$T(i,r) \le O(mn) + 2iT(i-1,r-1) + T(i-1,r)$$.
Given $$T(0,r) \le c_1$$ and $$T(i,0) \le c_1$$ for all $$i,r \ge 0$$, and $$T(i,r) \le c_2 + 2iT(i-1,r-1) + T(i-1,r)$$ for $$i,r \ge 1$$, where $$c_1=O(m)$$ and $$c_2=O(mn)$$.
It follows that $$T(i,r) \le c_2i + 2\sum_{j=1}^{i}jT(j-1,r-1)+c_1 \le c_1+c_2i+i(i+1)T(i,r-1)$$.
Solving this, $$T(i,r) < c_1+c_2(i+1)+(i+1)^2T(i,r-1)$$.
This leads to $$T(i,r) < c_2\sum_{j=0}^{r-1}(i+1)^{2j+1}+c_1\sum_{j=0}^{r}(i+1)^{2j} \le O(mn(i+1)^{2r-1}+m(i+1)^{2r})$$.
Since $$i \le n$$ and $$m=|S|$$, the time for FIND$$(S,r)$$ is $$O(|S|(n+1)^{2r})$$.

-----

### Theorem 1

Given a sample $$S$$ of a Boolean function on $$X_n$$, using FINDMIN(S) (which iteratively calls FIND$$(S,r)$$ for $$r=0,1,2,...$$ until a tree is returned), a decision tree consistent with $$S$$ and having rank $$r(S)$$ can be produced in time $$O(|S|(n+1)^{2r(S)})$$.


### Definition of Error in Learning

  * **Error of a hypothesis:** For a probability distribution $$P$$ on $$X_n$$ and a target Boolean function $$f$$ on $$X_n$$, the error of a hypothesis $$g$$ (w.r.t. $$f$$ and $$P$$) is the probability that $$f(x) \ne g(x)$$ for $$x$$ drawn randomly from $$X_n$$ according to $$P$$.

-----

### Lemma 4 (Blumer et al., 1987)

Let $$F_n$$ be a class of Boolean functions on $$X_n$$ and $$P$$ be a probability distribution on $$X_n$$. For any $$0 < \epsilon, \delta < 1$$, and any target function $$f$$ on $$X_n$$, given a sequence of at least $$\frac{1}{\epsilon}\ln\frac{|F_n|}{\delta}$$ random examples of $$f$$ (chosen independently according to $$P$$), with probability at least $$1-\delta$$, every hypothesis $$g \in F_n$$ that is consistent with all of these examples has error at most $$\epsilon$$.

**Proof of Lemma 4:**
For any single function with error at least $$\epsilon$$, the probability that it is consistent with $$m$$ random examples is at most $$(1-\epsilon)^m \le e^{-\epsilon m}$$. Hence, the probability that any function in $$F_n$$ that has error at least $$\epsilon$$ is consistent with $$m$$ random examples is at most $$|F_n|e^{-\epsilon m}$$. Setting this to $$\delta$$ and solving for $$m$$ gives the result.

-----

### Theorem 2

For any $$n \ge r \ge 1$$, any target function $$f \in F_n^r$$, any probability distribution $$P$$ on $$X_n$$, and any $$0 < \epsilon, \delta < 1$$, given a sample $$S$$ derived from a sequence of at least $$\frac{1}{\epsilon}((\frac{en}{r})^{r}\ln(8n)+\ln\frac{1}{\delta})$$ random examples of $$f$$ (chosen independently according to $$P$$), with probability at least $$1-\delta$$, FIND$$(S,r)$$ (or FINDMIN(S)) produces a hypothesis $$g \in F_n^r$$ that has error at most $$\epsilon$$.

**Proof of Theorem 2:**
By Lemma 1, $$|F_n^r| \le (8n)^{(\frac{en}{r})^r}$$ for $$n \ge r \ge 1$$. Hence by Lemma 4, with probability at least $$1-\delta$$, every hypothesis $$g \in F_n^r$$ consistent with $$S$$ has error at most $$\epsilon$$. Since FIND$$(S,r)$$ and FINDMIN(S) produce one of these hypotheses, the result follows.

-----

### Definition of $$F_n^{(s)}$$

  * $$F_n^{(s)}$$: The set of all Boolean functions on $$X_n$$ represented by decision trees with at most $$s$$ nodes.


### Lemma 5

For all $$n, s \ge 1$$, $$F_n^{(s)} \subseteq F_n^{\lfloor \log s \rfloor}$$.

**Proof of Lemma 5:**
In Lemma 1, it was shown that the smallest decision tree of rank $$r$$ has at least $$2^{r+1}-1$$ nodes. Thus, the rank of a decision tree with $$s$$ nodes is at most $$\log(s+1)-1 \le \lfloor \log s \rfloor$$.

-----

### Theorem 3

For any $$n, s \ge 1$$, where $$n \ge \lfloor \log s \rfloor \ge 1$$, any target function $$f \in F_n^{(s)}$$, any probability distribution $$P$$ on $$X_n$$, and any $$0 < \epsilon, \delta < 1$$, given a sample $$S$$ derived from a sequence of at least $$\frac{1}{\epsilon}((\frac{en}{\lfloor \log s \rfloor})^{\lfloor \log s \rfloor}\log(8n)+\ln\frac{1}{\delta})$$ random examples of $$f$$ (chosen independently according to $$P$$), with probability at least $$1-\delta$$, FINDMIN(S) produces a hypothesis $$g \in F_n^{\lfloor \log s \rfloor}$$ that has error at most $$\epsilon$$.

**Proof of Theorem 3:**
This follows directly from Theorem 2 and Lemma 5.

-----

### Corollary 1

Let $$p(n)$$ be any polynomial. There is a learning algorithm that, given random examples drawn according to any distribution on $${0,1}^n$$ of any target function represented by a decision tree on $$n$$ Boolean variables with at most $$p(n)$$ nodes, produces, with probability at least $$1-\delta$$, a hypothesis (represented as a decision tree) that has error at most $$\epsilon$$. The number of random examples and computation time required is linear in $$n^{O(\log n)}$$, $$1/\epsilon$$, and $$\log(1/\delta)$$.

**Proof of Corollary 1:**
This follows directly from Theorems 1 and 3.



