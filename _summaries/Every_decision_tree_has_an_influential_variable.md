---
layout: page
title: Every decision tree has an influential variable
description: title is self-explanatory
categories: [Summary, ActiveLearning]
img: assets/img/Every_decision_tree_has_an_influential_variable/img.png
importance: 1
giscus_comments: true
link: https://arxiv.org/abs/cs/0508071
---

This summary focuses exclusively on the technical aspects of the paper concerning boolean functions $$f:\{-1,1\}^{n}\rightarrow\{-1,1\}$$, including definitions, notations, the main theorem, and its proof as they apply to this specific case.

### Definitions and Notations

* **Input Domain:** The domain is $$\{-1,1\}^{n}_{(p)}$$, which represents $$n$$ binary input variables. The measure is taken with respect to an arbitrary product measure $$p$$ on $$\{-1,1\}^{n}$$. When written simply $$\{-1,1\}^{n}$$, the uniform measure case where $$p=1/2$$ is implied.
* **Function Output:** The output is binary, $$f:\{-1,1\}^{n}\rightarrow\{-1,1\}$$.
* **Variance ($$Var[f]$$):** For a function $$f:\{-1,1\}_{(p)}^{n}\rightarrow\{-1,1\}$$, the variance is defined as $$Var[f] = E[f^2] - E[f]^2 = 4 \Pr[f=1]\Pr[f=-1]$$. This measures the "balance" of the function.
* **Influence ($$Inf_{i}(f)$$):** The influence of the $$i$$-th coordinate on $$f$$ is defined as $$Inf_{i}(f) = 2 \Pr_{x,x^{(i)}}[f(x) \neq f(x^{(i)})]$$. Here, $$x$$ is drawn from $$\{-1,1\}_{(p)}^{n}$$ and $$x^{(i)}$$ is formed by rerandomizing the $$i$$-th coordinate of $$x$$ using the probability measure $$p_i$$. In the uniform measure case ($$p=1/2$$), this definition aligns with $$Inf_{i}[f] = \Pr[f(x) \ne f(x \oplus i)]$$.
* **DDT:** A decision tree.
* **Probability of Querying a Variable ($$\delta_{i}(T)$$):** For a DDT $$T$$ computing a function $$f:\{-1,1\}_{(p)}^{n}\rightarrow\{-1,1\}$$, $$\delta_{i}(T) = \Pr_{x\in\{-1,1\}_{(p)}^{n}}[T \text{ queries } x_{i}]$$.
* **Expected Cost ($$\Delta(T)$$):** For a DDT $$T$$, the expected cost is $$\Delta(T) = \sum_{i=1}^{n} \delta_{i}(T) = E[\text{#coords T queries on } x]$$.
* **Minimum Expected Cost ($$\Delta(f)$$):** $$\Delta(f)$$ denotes the minimum of $$\Delta(T)$$ over all DDTs $$T$$ computing $$f:\{-1,1\}_{(p)}^{n}\rightarrow\{-1,1\}$$.

### Main Theorems and Proofs

**Theorem 1.1:** Let $$f:\{-1,1\}_{(p)}^{n}\rightarrow\{-1,1\}$$ and let $$T$$ be a DDT computing $$f$$. Then


$$Var[f]\le\sum_{i=1}^{n}\delta_{i}(T)Inf_{i}(f).$$



**Proof of Theorem 1.1:**
Let $$x$$ and $$y$$ be random inputs chosen independently from $$\Omega = (\{-1,1\}^n, \mu_{(p)})$$. For a subset $$J\subseteq[n]$$, let $$x_{J}y$$ denote the hybrid input that agrees with $$x$$ on coordinates in $$J$$ and with $$y$$ on coordinates in $$[n]\setminus J$$.

Let $$i_1, \dots, i_s$$ be the sequence of variables queried by $$T$$ on input $$x$$. $$s$$ is a random variable representing the number of queried variables. For $$t \ge 0$$, let $$J[t] = \{i_r : s \ge r > t\}$$. It is the dimensions of the last $$s-t$$ node in the root to $$x$$ path.

last Define $$u[t] = x_{J[t]}y$$. $$u[t]$$ means the datapoint agreeing with $$x$$ on the last $$s-t$$ dimensions' of the nodes in the root to $$x$$ path and other dimensions are set to match that of $$y$$.

**We are slowly transforming $$x$$ to $$y$$ by slowly changing its dimension one by one to match that of $$y$$. We are doing it in a way that if in a step the label changed, that is counted in influence of some node. This is why we start from the bottom and go up. This way when a dimension changes if the labels also change, that is counted in influence of that node.**

We start with the observation that $$Var[f] = E[f(x) \neq f(y)] = E[f(u[0]) \neq f(u[s])]$$. This follows because $$y = u[s]$$ and $$f(x) = f(u[0])$$ as $$T$$ computes $$f$$.

$$E[f(u[0])\neq f(u[s])] \le E\left[\sum_{t=1}^{s} f(u[t-1])\neq  f(u[t])\right]$$

**The above inequality only means if $$f(x)\neq f(y)$$ the label should have changed somewhere in the process.** Notice that $$u[t-1]$$ and $$u[t]$$ differ only on one dimension assume $$i(t)$$. Splitting the expeted value based on $$i(t)$$, we get:

$$Var[f] \leq \sum_{t=1}^{n} \sum_{i=1}^{n} E[(f(u[t-1])\neq f(u[t]))\cdot 1_{\{i_t=i\}}]$$

We define $$X_t$$ as the sequence of variables that $$T$$ queries on $$x$$ till time $$t$$. $$X_t = (x_{i_1}, x_{i_2}, \cdots, x_{i_{\min(t, s)}})$$

$$Var[f] \leq \sum_{t=1}^{n} \sum_{i=1}^{n} E[E[(f(u[t-1])\neq f(u[t]))\cdot 1_{\{i_t=i\}}\mid X_{t-1}]]$$

Obviously, given the random variable $$X_{t-1}$$ we can determine the first $$t$$ node in the path thus determining $$i_t$$. Proof magic happened here: we can show that conditional on $$X_{t-1}$$, the pair $$(u[t-1], u[t])$$ has the distribution $$\Omega^{(i_t)}$$ if $$i_t = i \in [n]$$.


This is because $$u[t-1]$$ and $$u[t]$$ differ only along a single dimension, which is $$i(t)$$. Additionally, $$y$$ is unrelated to $$X_{t-1}$$, so its distribution is independent. In $$u[t] = x_{J[t]} y$$, the dimensions not contained in $$J[t]$$ are set to match those of $$y$$; therefore, they retain their original distribution $$\Omega$$.
The dimensions in $$J[t]$$ are set to those of $$x$$, specifically the $$t, t+1, \ldots, s$$-th dimensions along the root-to-$$x$$ path. These dimensions are distinct from the first $$t-1$$ dimensions of $$x$$ and thus also preserve their original distribution.
As a result, $$u[t]$$ is distributed according to $$\Omega^{(i_t)}$$ whenever $$i_t = i \in [n]$$.
This means:

$$E[(f(u[t-1])\neq f(u[t]))\cdot 1_{\{i_t=i\}\mid X_{t-1}]=E_{x, y \sim \Omega^{(i_t)}}[(f(x)\neq f(y))\cdot 1_{\{i_t(x)=i\}}]=Inf_i(f) 1_{i_t(x)=i}.$$

Using the above

$$Var[f] \leq \sum_{t=1}^{n} \sum_{i=1}^{n} E[Inf_i(f)\cdot 1_{\{i_t=i\}}] = \sum_{i=1}^{n} Inf_i(f)\sum_{t=1}^{n} E[1_{\{i_t=i\}}] = \sum_{i=1}^{n} Inf_i(f) \delta_i(T)$$



-----------------------------------------------
**Corollary 1.2:** For every $$f:\{-1,1\}_{(p)}^{n}\rightarrow\{-1,1\}$$, we have


$$\Delta(f)\ge\frac{Var(f)}{Inf_{max}(f)}$$


where $$Inf_{max}(f) = \max\{Inf_i(f) : i \in [n]\}$$.

**Proof of Corollary 1.2:**
Let $$T$$ be a DDT computing $$f$$. From Theorem 1.1:


$$Var[f]\le\sum_{i=1}^{n}\delta_{i}(T)Inf_{i}(f)$$




$$Var[f]\le Inf_{max}(f)\sum_{i=1}^{n}\delta_{i}(T) = Inf_{max}(f)\cdot\Delta(T)$$


Since this holds for any DDT $$T$$ computing $$f$$, it holds for the one minimizing $$\Delta(T)$$, which is $$\Delta(f)$$.
