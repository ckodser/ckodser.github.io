s=r"""
-----

layout: page
title: Learning Decision Trees from Random Examples - Technical Summary
description: Technical aspects of learning decision trees
categories: [Summary, DecisionTrees, LearningTheory]
img: assets/img/learning\_decision\_trees/img.png
importance: 1
giscus\_comments: true
link: [https://arxiv.org/abs/s2.0-0890540189900011-main](https://www.google.com/search?q=https://arxiv.org/abs/s2.0-0890540189900011-main)

-----

This summary focuses exclusively on the technical aspects of the paper concerning learning decision trees, including definitions, notations, the main theorems, and their proofs.

### Notational Conventions

  * **log**: Denotes the logarithm base 2[cite: 37].
  * **ln**: Denotes the natural logarithm[cite: 37].
  * **e**: Denotes the base of the natural logarithm[cite: 38].
  * **|S|**: Denotes the cardinality of set S[cite: 39].

### Definitions and Notations for Decision Trees

  * **Variables:** $V\_n = {v\_1, ..., v\_n}$ is a set of $n$ Boolean variables[cite: 40].
  * **Input Domain:** $X\_n = {0,1}^n$[cite: 41].
  * **Class of Decision Trees ($T\_n$):** Recursively defined as follows[cite: 41]:
      * A single root node labeled 0 or 1 is in $T\_n$ (abbreviated as "Q=0" or "Q=1")[cite: 41].
      * If $Q\_0, Q\_1 \\in T\_n$ and $v \\in V\_n$, then the binary tree with root labeled $v$, left subtree $Q\_0$ (0-subtree), and right subtree $Q\_1$ (1-subtree) is in $T\_n$[cite: 41].
  * **Boolean Function Representation ($f\_Q$):** A decision tree $Q \\in T\_n$ represents a Boolean function $f\_Q$[cite: 42]:
      * If $Q=0$, $f\_Q$ is the constant function 0[cite: 42].
      * If $Q=1$, $f\_Q$ is the constant function 1[cite: 42].
      * Else if $v\_i$ is the label of the root of Q, $Q\_0$ the 0-subtree, and $Q\_1$ the 1-subtree, then for $x=(a\_1, ..., a\_n) \\in {0,1}^n$, if $a\_i=0$ then $f\_Q(x)=f\_{Q\_0}(x)$, else $f\_Q(x)=f\_{Q\_1}(x)$[cite: 42].
  * **Reduced Decision Tree:** A decision tree where each variable appears at most once in any path from the root to a leaf[cite: 42].
  * **Rank of a Decision Tree ($r(Q)$):** Defined recursively[cite: 43]:
      * If $Q=0$ or $Q=1$, then $r(Q)=0$[cite: 43].
      * Else if $r\_0$ is the rank of the 0-subtree of Q and $r\_1$ is the rank of the 1-subtree, then $r(Q) = \\max(r\_0, r\_1)$ if $r\_0 \\ne r\_1$, and $r(Q) = r\_0+1 (=r\_1+1)$ otherwise[cite: 44].
  * $T\_n^r$: The set of all decision trees in $T\_n$ of rank at most $r$[cite: 45].
  * $F\_n^r$: The set of Boolean functions on $X\_n$ represented by trees in $T\_n^r$[cite: 45].

-----

### Lemma 1

(i) Let $k$ be the number of nodes in a reduced decision tree over $V\_n$ of rank $r$, where $n \\ge r \\ge 1$. Then $2^{r+1}-1 \\le k \\le (2\\sum\_{i=0}^{r}\\binom{n}{i})-1 \< 2(en/r)^r$[cite: 47].
(ii) If $r=0$ then $|F\_n^r|=2$. Else if $n \\le r$ then $|F\_n^r|=2^{2^n}$, and if $n \> r$ then $|F\_n^r| \\le (8n)^{(en/r)^r}$[cite: 48].

**Proof of Lemma 1:**
(i) By induction, the smallest decision tree of rank $r$ is a complete binary tree of depth $r$, which has $2^{r+1}-1$ nodes. Thus, $2^{r+1}-1 \\le k$[cite: 49, 50].
Let $L(n,r)$ be the maximum number of leaves of any reduced decision tree over $V\_n$ of rank $r$. From the definition of rank:
$L(0,r)=1$ for all $r \\ge 0$[cite: 51].
$L(n,0)=1$ for all $n \\ge 0$[cite: 51].
$L(n,r)=L(n-1,r)+L(n-1,r-1)$ for all $n,r \\ge 1$, because the variable in the root of a reduced tree does not appear in its subtrees[cite: 51].
The solution for this recurrence for $n \\ge r$ is $L(n,r)=\\sum\_{i=0}^{r}\\binom{n}{i}$, which is bounded by $(en/r)^r$ for $n \\ge r \\ge 1$[cite: 52]. Since a binary tree has one less internal node than leaves, this yields the second and third inequalities for $k$[cite: 53].

(ii) If $r=0$, $F\_n^r$ contains only constant functions, so $|F\_n^r|=2$[cite: 54, 55]. If $n \\le r$, $T\_n^r$ includes every full binary decision tree of depth $n$, so $F\_n^r$ includes all Boolean functions on $X\_n$, and thus $|F\_n^r|=2^{2^n}$[cite: 55, 56, 57]. If $n \> r \\ge 1$, each function in $F\_n^r$ is represented by a binary tree with at most $k=(en/r)^r$ leaves[cite: 57]. The number of distinct binary decision trees on $n$ variables with at most $k$ leaves is at most $\\sum\_{i=1}^{k}\\frac{2^{i}n^{i-1}}{2i-1}\\binom{2i-1}{i}\<(2n)^{k}\\sum\_{i=1}^{k}\\binom{2k-1}{i}\<(2n)^{k}2^{2k-1}\<(8n)^{k}$[cite: 58]. Therefore, $|F\_n^r| \\le (8n)^{(en/r)^r}$[cite: 58].

-----

### Definitions for Finding Consistent Decision Trees

  * **Example:** A pair $(x, f(x))$ for a Boolean function $f$ on $X\_n$[cite: 59]. It is positive if $f(x)=1$, else negative[cite: 59].
  * **Sample:** A set of examples of a function $f$[cite: 60]. $|S|$ denotes the number of examples in $S$[cite: 61].
  * **Consistent Decision Tree:** A decision tree $Q \\in T\_n$ (or $f\_Q$) is consistent with a sample $S$ if for any example $(x, f(x))$ in $S$, $f(x)=f\_Q(x)$[cite: 61].
  * **Rank of a Sample ($r(S)$):** The minimum rank of any decision tree consistent with $S$[cite: 61].
  * **$S\_0^v$ and $S\_1^v$:** For a sample $S$ of a function $f$ on $X\_n$ and variable $v=v\_i \\in V\_n$:
      * $S\_0^v$ is the set of examples $(x, f(x))$ in $S$ where $x=(a\_1, ..., a\_n)$ and $a\_i=0$[cite: 62].
      * $S\_1^v$ is the set of examples $(x, f(x))$ in $S$ where $x=(a\_1, ..., a\_n)$ and $a\_i=1$[cite: 62].
  * **Informative Variable:** A variable $v$ is informative on $S$ if both $S\_0^v$ and $S\_1^v$ are nonempty[cite: 62].

### Procedure FIND(S, r)

**Input:** A nonempty sample $S$ of some Boolean function on $X\_n$ and an integer $r \\ge 0$[cite: 62, 63].
**Output:** A decision tree of rank at most $r$ consistent with $S$ if one exists, else "none"[cite: 63].

1.  If all examples in $S$ are positive, return $Q=1$; if all are negative, return $Q=0$[cite: 63].
2.  If $r=0$, return "none"[cite: 63].
3.  For each informative variable $v \\in V\_n$:
    A. Let $Q\_0^v = \\text{FIND}(S\_0^v, r-1)$ and $Q\_1^v = \\text{FIND}(S\_1^v, r-1)$[cite: 63].
    B. If both recursive calls succeed (neither $Q\_0^v=\\text{none}$ nor $Q\_1^v=\\text{none}$), return the decision tree with root labeled $v$, 0-subtree $Q\_0^v$, and 1-subtree $Q\_1^v$[cite: 63].
    C. If one recursive call succeeds but the other does not:
    1\. Reexecute the unsuccessful call with rank bound $r$ instead of $r-1$ (e.g., if $Q\_1^v$ is a tree but $Q\_0^v=\\text{none}$, let $Q\_0^v = \\text{FIND}(S\_0^v, r)$)[cite: 64].
    2\. If the reexecuted call succeeds, let $Q$ be the decision tree with root labeled $v$, 0-subtree $Q\_0^v$, and 1-subtree $Q\_1^v$, else let $Q=\\text{"none"}$[cite: 64].
    3\. Return $Q$[cite: 65].
4.  Return "none"[cite: 65].

-----

### Lemma 2 (Correctness of FIND)

The procedure FIND is correct[cite: 65].

**Proof of Lemma 2:**
Let $m=|S|$. Correctness is by induction on $m$ and $r$[cite: 66].
If $m=1$ or $r=0$, FIND$(S,r)$ is easily verified to be correct[cite: 67].
Assume $S$ has $|S|=m \\ge 2$ and $r \\ge 1$. Assume the procedure is correct for $r-1$ with arbitrary size $S$, and for $r$ when $S$ has size less than $m$[cite: 68].
Since $|S\_0^v| \< |S|$ and $|S\_1^v| \< |S|$ for any informative variable $v$, if FIND$(S,r)$ returns a tree (in step 1, 3B, or 3C), by the inductive hypothesis and definition of rank, it will be a tree of rank at most $r$ consistent with $S$[cite: 69].
If "none" is returned and $r \\ge 1$, execution stops in step 3C or 4[cite: 69]. If in 3C, by induction, either $r(S\_0^v) \> r$ or $r(S\_1^v) \> r$ for some $v$, implying $r(S) \> r$[cite: 69, 70]. If in step 4, by induction, $r(S\_0^v) \\ge r$ and $r(S\_1^v) \\ge r$ for every informative variable $v$[cite: 70]. As execution didn't halt at step 1, any decision tree consistent with $S$ must have a variable at its root[cite: 70]. Let $Q$ be a minimal-node decision tree of rank $r(S)$ consistent with $S$[cite: 71]. Its root must be an informative variable $v$[cite: 72]. The 0-subtree must be consistent with $S\_0^v$ (where $r(S\_0^v) \\ge r$) and the 1-subtree with $S\_1^v$ (where $r(S\_1^v) \\ge r$)[cite: 72]. Thus, both subtrees must have rank at least $r$, implying $r(Q) \> r$ by definition of rank[cite: 72, 73]. Thus $r(S) \> r$[cite: 73]. Hence, the procedure is correct in all cases[cite: 73].

-----

### Lemma 3 (Time of FIND)

For any nonempty sample $S$ of a function on $X\_n$ and $r \\ge 0$, the time of FIND$(S,r)$ is $O(|S|(n+1)^{2r})$[cite: 74].

**Proof of Lemma 3:**
Let $T(i,r)$ be the max time for FIND$(S,r)$ when $S$ is a sample on $X\_n$ with $1 \\le |S| \\le m$ and at most $i$ variables are informative[cite: 75].
If $i=0$, $T(i,r)$ is $O(1)$ (since $|S|=1$)[cite: 75]. If $r=0$, $T(i,r)$ is $O(m)$[cite: 76].
For $r \\ge 1$, steps 1 and 3 (determining informative variables) take $O(mn)$ time[cite: 76]. Each of the two recursive calls in step 3A takes at most $T(i-1, r-1)$ time, as $v$ is no longer informative[cite: 76]. These calls are made at most $i$ times, totaling $2iT(i-1, r-1)$ for step 3A[cite: 77]. Step 3C.1 makes at most one recursive call to $FIND(S\_0^v, r)$ or $FIND(S\_1^v, r)$, taking at most $T(i-1, r)$ time[cite: 77, 78].
Therefore, for $r \\ge 1$: $T(i,r) \\le O(mn) + 2iT(i-1,r-1) + T(i-1,r)$[cite: 79].
Given $T(0,r) \\le c\_1$ and $T(i,0) \\le c\_1$ for all $i,r \\ge 0$, and $T(i,r) \\le c\_2 + 2iT(i-1,r-1) + T(i-1,r)$ for $i,r \\ge 1$, where $c\_1=O(m)$ and $c\_2=O(mn)$[cite: 79].
It follows that $T(i,r) \\le c\_2i + 2\\sum\_{j=1}^{i}jT(j-1,r-1)+c\_1 \\le c\_1+c\_2i+i(i+1)T(i,r-1)$[cite: 80].
Solving this, $T(i,r) \< c\_1+c\_2(i+1)+(i+1)^2T(i,r-1)$[cite: 80].
This leads to $T(i,r) \< c\_2\\sum\_{j=0}^{r-1}(i+1)^{2j+1}+c\_1\\sum\_{j=0}^{r}(i+1)^{2j} \\le O(mn(i+1)^{2r-1}+m(i+1)^{2r})$[cite: 80].
Since $i \\le n$ and $m=|S|$, the time for FIND$(S,r)$ is $O(|S|(n+1)^{2r})$[cite: 80].

-----

### Theorem 1

Given a sample $S$ of a Boolean function on $X\_n$, using FINDMIN(S) (which iteratively calls FIND$(S,r)$ for $r=0,1,2,...$ until a tree is returned), a decision tree consistent with $S$ and having rank $r(S)$ can be produced in time $O(|S|(n+1)^{2r(S)})$[cite: 81, 82].

-----

### Definition of Error in Learning

  * **Error of a hypothesis:** For a probability distribution $P$ on $X\_n$ and a target Boolean function $f$ on $X\_n$, the error of a hypothesis $g$ (w.r.t. $f$ and $P$) is the probability that $f(x) \\ne g(x)$ for $x$ drawn randomly from $X\_n$ according to $P$[cite: 84].

-----

### Lemma 4 (Blumer et al., 1987)

Let $F\_n$ be a class of Boolean functions on $X\_n$ and $P$ be a probability distribution on $X\_n$. For any $0 \< \\epsilon, \\delta \< 1$, and any target function $f$ on $X\_n$, given a sequence of at least $\\frac{1}{\\epsilon}\\ln\\frac{|F\_n|}{\\delta}$ random examples of $f$ (chosen independently according to $P$), with probability at least $1-\\delta$, every hypothesis $g \\in F\_n$ that is consistent with all of these examples has error at most $\\epsilon$[cite: 85].

**Proof of Lemma 4:**
For any single function with error at least $\\epsilon$, the probability that it is consistent with $m$ random examples is at most $(1-\\epsilon)^m \\le e^{-\\epsilon m}$[cite: 86]. Hence, the probability that any function in $F\_n$ that has error at least $\\epsilon$ is consistent with $m$ random examples is at most $|F\_n|e^{-\\epsilon m}$[cite: 86]. Setting this to $\\delta$ and solving for $m$ gives the result[cite: 86].

-----

### Theorem 2

For any $n \\ge r \\ge 1$, any target function $f \\in F\_n^r$, any probability distribution $P$ on $X\_n$, and any $0 \< \\epsilon, \\delta \< 1$, given a sample $S$ derived from a sequence of at least $\\frac{1}{\\epsilon}((\\frac{en}{r})^{r}\\ln(8n)+\\ln\\frac{1}{\\delta})$ random examples of $f$ (chosen independently according to $P$), with probability at least $1-\\delta$, FIND$(S,r)$ (or FINDMIN(S)) produces a hypothesis $g \\in F\_n^r$ that has error at most $\\epsilon$[cite: 87].

**Proof of Theorem 2:**
By Lemma 1, $|F\_n^r| \\le (8n)^{(en/r)^r}$ for $n \\ge r \\ge 1$[cite: 88]. Hence by Lemma 4, with probability at least $1-\\delta$, every hypothesis $g \\in F\_n^r$ consistent with $S$ has error at most $\\epsilon$[cite: 88]. Since FIND$(S,r)$ and FINDMIN(S) produce one of these hypotheses, the result follows[cite: 89].

-----

### Definition of $F\_n^{(s)}$

  * $F\_n^{(s)}$: The set of all Boolean functions on $X\_n$ represented by decision trees with at most $s$ nodes[cite: 93].

-----

### Lemma 5

For all $n, s \\ge 1$, $F\_n^{(s)} \\subseteq F\_n^{\\lfloor \\log s \\rfloor}$[cite: 94].

**Proof of Lemma 5:**
In Lemma 1, it was shown that the smallest decision tree of rank $r$ has at least $2^{r+1}-1$ nodes[cite: 95]. Thus, the rank of a decision tree with $s$ nodes is at most $\\log(s+1)-1 \\le \\lfloor \\log s \\rfloor$[cite: 96].

-----

### Theorem 3

For any $n, s \\ge 1$, where $n \\ge \\lfloor \\log s \\rfloor \\ge 1$, any target function $f \\in F\_n^{(s)}$, any probability distribution $P$ on $X\_n$, and any $0 \< \\epsilon, \\delta \< 1$, given a sample $S$ derived from a sequence of at least $\\frac{1}{\\epsilon}((\\frac{en}{\\lfloor \\log s \\rfloor})^{\\lfloor \\log s \\rfloor}\\log(8n)+\\ln\\frac{1}{\\delta})$ random examples of $f$ (chosen independently according to $P$), with probability at least $1-\\delta$, FINDMIN(S) produces a hypothesis $g \\in F\_n^{\\lfloor \\log s \\rfloor}$ that has error at most $\\epsilon$[cite: 96, 97].

**Proof of Theorem 3:**
This follows directly from Theorem 2 and Lemma 5[cite: 97, 98].

-----

### Corollary 1

Let $p(n)$ be any polynomial. There is a learning algorithm that, given random examples drawn according to any distribution on ${0,1}^n$ of any target function represented by a decision tree on $n$ Boolean variables with at most $p(n)$ nodes, produces, with probability at least $1-\\delta$, a hypothesis (represented as a decision tree) that has error at most $\\epsilon$. The number of random examples and computation time required is linear in $n^{O(\\log n)}$, $1/\\epsilon$, and $\\log(1/\\delta)$[cite: 98, 99].

**Proof of Corollary 1:**
This follows directly from Theorems 1 and 3[cite: 99].

-----

### Definitions for DNF Expressions

  * **Literals ($L\_n$):** For $V\_n = {v\_1, ..., v\_n}$, $L\_n = {v\_1, ..., v\_n, \\bar{v}\_1, ..., \\bar{v}\_n}$ (variables or negated variables)[cite: 100].
  * **Term:** A conjunction $t = l\_1 \\dots l\_q$, where $q \> 0$ and $l\_i \\in L\_n$[cite: 100]. If $q=0$, the term represents the constant function 1[cite: 100]. Assume no term contains both a variable and its negation, and no term contains the same literal more than once[cite: 101].
  * **DNF Expression:** A disjunction $\\phi = t\_1 \\lor \\dots \\lor t\_r$ of terms on $V\_n$, where $r \> 0$[cite: 100, 101]. If $r=0$, $\\phi$ represents the constant function 0[cite: 101].
  * **Representing a Boolean Function ($f$ by $(\\phi, \\psi)$):** A pair of DNF expressions $(\\phi, \\psi)$ on $V\_n$ represents a Boolean function $f$ on $X\_n$ if for all $x \\in X\_n$, $f(x)=1$ if and only if $x$ satisfies $\\phi$, and $f(x)=0$ if and only if $x$ satisfies $\\psi$[cite: 102, 103].
  * **Restriction of $f$ to $v\_i=0$ ($f|\_{v\_i=0}$):** The Boolean function on ${0,1}^{n-1}$ defined by $f|*{v\_i=0}(a\_1, ..., a*{i-1}, a\_i, ..., a\_{n-1}) = f((a\_1, ..., a\_{i-1}, 0, a\_i, ..., a\_{n-1}))$[cite: 104].
  * **Restriction of $f$ to $v\_i=1$ ($f|\_{v\_i=1}$):** Defined similarly by setting the $i$-th index to 1[cite: 105].
"""


import re

def format_math_strings(text):
  """
  Replaces math delimiters in a string according to specified rules.

  Args:
    text: The input string.

  Returns:
    The modified string.
  """


  text = re.sub(r'\[cite:\s*(\d+\s*(,\s*\d+\s*)*)\]', '', text)
  dd=" "
  # Replace $$...$$ with \n$$...$$\n
  text = re.sub(r'\$\$(.*?)\$\$', dd+r'$$\1$$'+dd, text)

  # Replace $...$ with $$...$$
  text = re.sub(r'\$(.*?)\$', r'$$\1$$', text)

  # Replace $$$$ with $$
  text = re.sub(r'\$\$\$\$', r'$$', text)
  return text

# Example usage:
output_string = format_math_strings(s)
print(output_string)
