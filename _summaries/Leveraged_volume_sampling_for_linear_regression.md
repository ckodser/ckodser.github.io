---
layout: page
title: Leveraged volume sampling for linear regression
description: Active Learning in linear regression with multiplicative error rate bounds
categories: [Summary, ActiveLearning]
img: assets/img/Leveraged_volume_sampling_for_linear_regression/img.png
importance: 1
giscus_comments: true
link: https://arxiv.org/abs/1802.06749
---

They want to find a linear regression that its loss (square loss) is at most $$1+\epsilon$$ times the best regression.
They show that they can achieve this with
$$O\left(d \log d + \frac{d}{\epsilon}\right)$$
labels with high probability.

<h1> Notation </h1>

input matrix $$X \in \mathbb{R}^{n \times d}$$ has (full) rank $$d$$. $$y \in \mathbb{R}^n$$ is the target vector. The goal of the learner is to find a weight vector $$w \in \mathbb{R}^d$$ that minimizes
the square loss:
$$w^* = arg\min_{w \in \mathbb{R}^d} \mathcal{L}(w),$$
where $$\mathcal{L}(w) = \sum_{i=1}^n (x_i^\top w - y_i)^2 = \\\lvert X w - y\ \\rvert_2^2.$$

Given both matrix $$X$$ and vector $$y$$, the least squares solution can be directly computed as $$w_* = X^+ y$$, where $$X^+$$ is the pseudo-inverse.

<h1> Standard volume sampling </h1>

Given $$X \in \mathbb{R}^{n \times d}$$ and a size $$k \geq d$$, standard volume sampling jointly chooses a set $$S$$ of $$k$$ indices in $$[n]$$ with probability

$$\Pr(S) = \frac{\det(X_S^T X_S)}{\binom{n-d}{k-d} \det(X^T X)}$$

after getting target value of set $$S$$, we set  $$w^*_{S} = (X_S)^+ y_S$$.

The main property of this approach is that
$$
\mathbb{E}[w^*_S] = w^*
$$.

They have shown that this approach can not grantee any $$1+\epsilon$$ multiplicative error rate with out checking labels of half of the data points in some cases.

<h1> Rescaled volume sampling </h1>

Define  $$l_i = x_i^{\top}(X^{\top}X)^{-1}x_i$$ and  $$q_i = \frac{l_i}{d}$$.

Sample $$k$$ row indices  $$\pi_1, \ldots, \pi_k$$ with replacement from $$\{1, \ldots, n\}$$ according to

$$
\Pr(\pi) \sim \det \left( \sum_{i=1}^k \frac{1}{q_{\pi_i}} x_{\pi_i} x_{\pi_i}^\top \right) \prod_{i=1}^k q_{\pi_i}.
$$

Define $$Q_{\pi} = \sum_{i=1}^k \frac{1}{q_{\pi_i}} \mathbf{e}_{\pi_i} \mathbf{e}_{\pi_i}^\top \in \mathbb{R}^{n \times n}$$

A good classifier is calculated from

$$w_*^{\pi} = \arg \min_{w \in \mathbb{R}^d}  \left\\\lvert Q_{\pi}^{\frac{1}{2}} (X w - y) \right\ \\rvert_2^2$$

And if $$k \in O(d \ln (\frac{d}{\delta}) + \frac{d}{\epsilon \delta})$$ the produced model will have a loss less than $$1+\epsilon$$ times the best regression with probability at least $$1 - \delta$$.
