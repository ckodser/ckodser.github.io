---
layout: page
title: Properly learning decision trees in almost polynomial time
description: learning a decision tree for unifrom random data distribution in O(s ^ log(log(s)))
categories: [Summary, ActiveLearning]
img: assets/img/Properly_learning _decision_trees_in_almost_polynomial_time/img.png
importance: 1
giscus_comments: true
link: https://arxiv.org/abs/2109.00637
---


### **Definitions**

#### **1. Decision Tree**
- **Size of the tree**: The number of leaves in the tree.
- **Depth of the tree**: The length of the longest root-to-leaf path.
- **Average Depth**: Defined as:
      <center>
   $$
   \Delta(T) := E_{x \sim \{\pm1\}^n}[\text{Depth of leaf that } x \text{ reaches}] =\text{for uniform data distribution}: \sum_{\text{leaves } \ell \in T} 2^{-\text{depth}(\ell)} \cdot \text{depth}(\ell).
   $$</center>
   For a size-$$s$$ tree (on uniform data distribution), $$ \Delta(T) \leq \log s$$.
- **A restriction**: A restriction $$\pi$$ of a function $$f : \{\pm1\}^n \to \{\pm1\}$$, denoted $$f_\pi$$,  
is the subfunction of $$f$$ that one obtains by fixing a subset of the variables to constants (i.e. $$x_i = b$$ for $$i \in [n]$$ and $$b \in \{\pm1\}$$). We write $$|\pi|$$ to denote the number of variables fixed by $$\pi$$.
- We define $$n$$ as the number of input dimensions.

---

#### **2. Influence of a Variable**
The **influence** of a variable $$x_i$$ with respect to a function $$f : \{\pm1\}^n \to \{\pm1\}$$ is defined as:
<center>
$$
\text{Inf}_i(f) := \Pr_{x \sim \{\pm1\}^n}[f(x) \neq f(x^{\sim i})],
$$</center>  
where $$x^{\sim i}$$ denotes $$x$$ with the $$i$$-th variable rerandomized (flipped with probability $$ \frac{1}{2}$$).

---

### **Pruning a Decision Tree**

Our Goal is to find a pruned version of our decision tree such that  
1. The size and depth of the pruned tree are no larger than the original.
2. The pruned tree is **everywhere $$\tau$$-influential**, meaning every variable queried at each node in the tree has influence at least $$\tau$$.

#### **Theorem 4 (Pruning Lemma for the Realizable Setting)**


Let $$f$$ be computable by a size-$$s$$ decision tree $$T$$, and let $$ \tau > 0$$. There exists a **pruning** $$\textbf{T}^*$$ of $$T$$ satisfying the following:

1. **Error Bound**:
      <center>$$
      \Pr_{x \sim \{\pm1\}^n}\big[f(x) \neq T^*(x)\big] \leq \tau \log s.
      $$ </center>
2. **Influence of Variables**:
      For every node $$v$$ in $$T^*$$, let $$i(v)$$ denote the variable queried at $$v$$. Then:
      <center>$$
      \text{Inf}_{i(v)}(f_v) \geq \tau,
      $$</center>  
      where $$f_v$$ is the restriction of $$f$$ along the root-to-$$v$$ path in $$T^*$$.

> This is because 
> start from the root and do pruning recursively, first prune the root if it is not influential, then recursively prune the left subtree, then prune the right subtree.
> There are two cases:
> 1. If the root is $$\tau$$-influential:
    If the root is $$\tau$$-influential, then we prune left and right subtree recursively. When both sides are $$\tau$$-influential, and the root is also $$\tau$$-influential, then the whole tree is $$\tau$$-influential.  
    The error of the resulting tree is equal to
    <center>$$\Pr_{x \sim \{\pm1\}^n}\big[f(x) \neq T^*(x)\big]   =$$</center>  
    Defining $$P_l:=\Pr_{x \sim \{\pm1\}^n}[x_{i(\text{root})}=-1]$$ and $$P_r:=\Pr_{x \sim \{\pm1\}^n}[x_{i(\text{root})}=1]$$, we have
    <center>$$P_l\cdot \Pr_{x \sim \{\pm1\}^n |x_{i(\text{root})}=-1}\big[f(x) \neq T^*_l(x)\big] + P_r\cdot \Pr_{x \sim \{\pm1\}^n |x_{i(\text{root})}=+1}\big[f(x) \neq T^*_r(x)\big]$$</center>  
    From the theorem we know that pruning subtrees is accurate so the error of the resulting tree is less than
    <center>$$\leq P_l\cdot \tau \log s + P_r\cdot \tau \log s = \tau \log s$$</center>  
> 2.  If the root is not $$\tau$$-influential: We have to remove the root along one of its subtrees and then recursively prune the remaining subtree.  
    It is clear that the resulting tree is $$\tau$$-influential. We calculate the error of the resulting tree in two steps. Assume we remove left subtree. $$x^{!i}$$ denotes $$x$$ with the $$i$$-th variable flipped.
    <center>$$\Pr_{x \sim \{\pm1\}^n}\big[f(x) \neq T^*(x)\big]   =$$</center>  
    Defining $$P_l:=\Pr_{x \sim \{\pm1\}^n}[x_{i(\text{root})}=-1]$$ and $$P_r:=\Pr_{x \sim \{\pm1\}^n}[x_{i(\text{root})}=1]$$, we have
    <center>$$P_l\cdot \Pr_{x \sim \{\pm1\}^n |x_{i(\text{root})}=-1}\big[f(x) \neq T^*_r(x^{!i})\big] + P_r\cdot \Pr_{x \sim \{\pm1\}^n |x_{i(\text{root})}=+1}\big[f(x) \neq T^*_r(x)\big]$$</center>
    <center>$$\leq P_l\cdot \Pr_{x \sim \{\pm1\}^n |x_{i(\text{root})}=-1}\big[f(x) \neq T^*_r(x^{!i})\big] + P_r\cdot \tau \log s$$</center>  
    cases where $$f(x) \neq T^*_r(x^{!i})$$ are two groups.  
    1. $$f(x) = f(x^{!i})$$ so $$f(x^{!i}) \neq T^*_r(x^{!i})$$ These samples should not be that large since $$f_r(x)$$ is approximate by $$T^*_r(x)$$.
    <center>$$ \Pr_{x \sim \{\pm1\}^n |x_{i(\text{root})}=-1}\big[f(x) \neq T^*_r(x^{!i})\big] \text{ and }   \big[f(x) = f(x^{!i})\big] \leq $$ </center>
    <center>$$ \Pr_{x \sim \{\pm1\}^n |x_{i(\text{root})}=-1} \big[f(x^{!i}) \neq T^*_r(x^{!i})]\big] \leq \tau \log s $$ </center>
    2. $$f(x) \neq f(x^{!i})$$ so $$f(x^{!i}) = T^*_r(x^{!i})$$  
    These are the samples that effected the influence of the root, so intuitively since the root influence is low, their number should not be too large.
    <center>$$ \Pr_{x \sim \{\pm1\}^n |x_{i(\text{root})}=-1}\big[f(x) \neq T^*_r(x^{!i})\big] \text{ and } \big[f(x) \neq f(x^{!i})\big] \leq $$ </center>
    <center>$$ \Pr_{x \sim \{\pm1\}^n |x_{i(\text{root})}=-1} \big[f(x) \neq f(x^{!i})\big] = $$ </center>  
    if $$f(x) \neq f(x^{!i})$$ then $$f(x^{!i}) \neq f(x)$$ so it is equal to  
    <center>$$ \Pr_{x \sim \{\pm1\}^n} \big[f(x) \neq f(x^{!i})\big] = 2\text{inf}_{i}(f)$$ </center>  
    since we don't rerandomize but force the change.
    combining these we have the error is less than
    <center> $$\leq P_l\cdot (2\text{inf}_{i}(f) + \tau \log (s/2)) + P_r\cdot \tau \log (s/2) \leq$$ </center>
    <center> $$\leq P_l\cdot (2\tau + \tau \log (s/2)) + P_r\cdot \tau \log (s/2)$$ </center>  
    Given that $$P_l=P_r=1/2$$, we have
    <center>$$= \tau+ \tau \log (s/2) = \tau \log s$$</center>  

---

#### **How it is used?**

**Bound on Influential Variables**:
     In the realizable setting + uniform data distribution:
     - The total influence of a size-$$s$$ decision tree is bounded by $$ \log s$$.
> This is because  
      <center>$$ \text{total influence} = \sum_i \text{Inf}_i(f) = \sum_i E_{x \sim \{\pm1\}^n}[ f(x) \neq f(x^{\sim i})]=E_{x \sim \{\pm1\}^n}[\sum_i f(x) \neq f(x^{\sim i})] =$$ </center>
      if $$i$$ is not queried in any node from root to leaf $$x$$ reaches then $$f(x) = f(x^{\sim i})$$. So it is equal to
      <center>$$E_{x \sim \{\pm1\}^n}[\sum_{i \in [i(v) \text{ for } v \text{ in path root to leaf that } x \text{ reaches}] } f(x) \neq f(x^{\sim i})] $$ </center>
      If we think about the effect of each $$v$$ in this we have
      <center>$$ \sum_{v \in \text{Tree}} P_{x \sim \{\pm1\}^n }[x \text{ reaches } v] \cdot E_{x \sim \text{subtree of } v }[ f(x) \neq f(x^{\sim i(v)})] = \sum_{v \in \text{Tree}} P_{x \sim \{\pm1\}^n }[x \text{ reaches } v] \cdot \text{inf}_{i(v)}(f_v)$$ </center>
      Since $$\text{inf}$$ is always less than $$1$$.
      <center>$$ \leq \sum_{v \in \text{Tree}} P_{x \sim \{\pm1\}^n }[x \text{ reaches } v]$$ </center>
      If we switch back and check how many nodes a sample has effect on we get
      <center>$$= E_{x \sim \{\pm1\}^n}[\text{Depth of leaf that } x \text{ reaches}] = \Delta(f)$$ </center>
      For unifrom data distribution this is less than $$ \log s$$.


  - Therefore, the number of variables with influence $$ \geq \tau$$ is at most $$(\log s)/\tau$$.  
  - If we set $$ \tau=\frac{\epsilon}{\log s}$$, Then using theorem 4, there exists a decision tree where each node is $$ \frac{\epsilon}{\log s}$$-influential and the error of the tree is less than $$ \epsilon$$. We try to find that recursively.
  - In each step, we need to find the best tree on $$f_\pi$$ and has a size less than $$s$$ for all those sizes. For each of these we need to check $$(\log s)/\tau = \frac{\log^2 s}{\epsilon}$$ dimensions.  
  - We can easily remove any node with depth more than $$d=\log(s/\epsilon)$$. This is because the error of doing so would be at most $$ \epsilon$$.So the run time will be:

> There is an algorithm which, given as input $$ \varepsilon > 0$$, $$s \in \mathbb{N}$$, and query access to a size-$$s$$ decision tree $$f : \{\pm 1\}^n 	\to \{\pm 1\}$$, runs in time
    <center>$$ \widetilde{O}(n^2) \cdot \left(\frac{s}{\varepsilon} \right)^{O\left(\log \left(\frac{\log s}{\varepsilon} \right)\right)} $$ </center>  
    and outputs a size-$$s$$ decision tree hypothesis $$T$$ that, with high probability, satisfies
    $$ \mathrm{dist}(T, f) \leq \varepsilon. $$


The proof of the runtime algorithm is as follows:
> The number of restrictions is   
    <center>$$ n\cdot\sum_{k=1}^{d} \left(\frac{\log^2 s}{\epsilon} \right)^k = n \cdot\left(\frac{\log^2 s}{\epsilon} \right)^{O(d)}. $$ </center> 
    We assumed that variable influences can be computed exactly in unit time, whereas in actuality, we can only obtain estimates of these quantities via random sampling. By inspection of our proofs, it suffices for these estimates to be accurate to $$\pm\tau/2$$. Query access to $$f$$ provides us with query access to $$f_\pi$$ for any $$\pi$$, and hence by the Chernoff bound, we can estimate $$\text{Inf}_i(f_\pi)$$ to accuracy $$\pm \tau/2$$ and with confidence $$1-\delta$$ using $$O(\log(1/\delta)/\tau^2)$$ queries and in $$O(\log(1/\delta)/\tau^2)$$ time.
    The number of times variables' influences are computed throughout the execution of the algorithm is at most  
    <center>$$n \cdot\left( \frac{\log^2 s}{\epsilon} \right)^{O(d)}$$</center>
    and so by setting $$ \delta < 1/\left(n \cdot ((\log^2 s)/\epsilon)^{O(d)}\right)$$, we ensure that w.h.p. all our estimates are indeed accurate to within $$\pm \tau/2$$.
    The overall runtime of our algorithm is
    <center>$$ n \cdot s^2 \cdot \left(\frac{\log^2 s}{\epsilon}\right)^{O(d)} \cdot \frac{n \log^2 s}{\epsilon^2} \left(\log n + d \log \left(\frac{\log^2 s}{\epsilon} \right)\right)= $$ </center>
    <center>$$n \cdot s^2 \cdot \left( \frac{\log^2 s}{\epsilon}\right)^{O(\log(s / \epsilon))} \cdot \frac{n \log^2 s}{\epsilon^2} \left( \log n + \log(s / \epsilon) \log \left( \frac{\log^2 s}{\epsilon}\right)\right)=$$ </center>
    <center>$$n^2 \cdot \frac{s^2}{\epsilon} \cdot \left( \frac{\log^2 s}{\epsilon}\right)^{O(\log(s / \epsilon))} \cdot \left( \log n + \log(s / \epsilon) \log \left( \frac{\log^2 s}{\epsilon}\right)\right)\leq$$ </center>
    <center>$$\tilde{O}\left( n^2 \cdot \frac{s^2}{\epsilon} \cdot \exp\left( \log\left(\frac{\log^2 s}{\epsilon}\right)\cdot O(\log(s / \epsilon))\right) \right) \leq $$ </center>
    <center>$$ \tilde{O}\left( n^2 \cdot \frac{s^2}{\epsilon} \cdot \exp\left( (2\log(\log s)- \log(\epsilon)) \cdot O(\log(s / \epsilon))\right) \right)$$ </center>
    Somehow it simplifies to  
    <center> $$ \leq \tilde{O}\left( n^2 \cdot \frac{s}{\epsilon} \cdot s^{O(\log (\log s)/\epsilon)}\right),$$ </center>
    and this completes the proof.

---

#### **Agnostic Setting**:

### **Extension to the Agnostic Setting**

In the agnostic setting (where $$f$$ may not exactly correspond to a size-$$s$$ decision tree):
- The number of influential variables is no longer bounded by $$(\log s)/\tau$$. It can be as large as $$ \Omega(n)$$.
- The algorithm employs **smoothing** of $$f$$ and **noisy influence** measures:
   - After smoothing $$f$$ with noise parameter $$\delta$$, the smoothed function $$\tilde{f}$$ is $$(\delta \log s)$$-close to $$f$$, and the set of variables with noisy influence $$\geq \tau$$ is bounded by $$1/(\tau \delta)$$.

These ideas enable an agnostic algorithm that achieves accuracy $$O(\text{opt}) + \epsilon$$.