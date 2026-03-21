---
layout: page
title: Active Learning for Decision Trees with Provable Guarantees
description: First polylogarithmic label complexity bounds for actively learning decision trees with multiplicative error guarantees
img: assets/img/active-learning-dt/decision_tree.png
importance: 1
giscus_comments: true
category: Active Learning
link: https://arxiv.org/abs/2601.20775
_styles: >
  .hero-section {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 2rem;
    color: #fff;
    position: relative;
    overflow: hidden;
  }
  .hero-section::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 70% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 50%);
    pointer-events: none;
  }
  .hero-section h2 {
    color: #fff;
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.7;
  }
  .hero-section .venue {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 4px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 1rem;
  }
  .hero-section .authors {
    font-size: 0.95rem;
    color: #d4d4f7;
    margin-bottom: 0.3rem;
  }
  .hero-section .affiliation {
    font-size: 0.85rem;
    color: #a8a8d0;
  }
  .result-card {
    border: 1px solid rgba(102, 126, 234, 0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    background: rgba(102, 126, 234, 0.03);
    transition: border-color 0.3s ease;
  }
  .result-card:hover {
    border-color: rgba(102, 126, 234, 0.4);
  }
  .result-card h4 {
    margin-top: 0;
    color: #667eea;
    font-size: 1rem;
    font-weight: 600;
  }
  .result-card .theorem-label {
    display: inline-block;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }
  .contribution-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
  }
  .contribution-item {
    border: 1px solid rgba(102, 126, 234, 0.15);
    border-radius: 12px;
    padding: 1.2rem;
    background: rgba(102, 126, 234, 0.02);
    transition: transform 0.2s ease, border-color 0.3s ease;
  }
  .contribution-item:hover {
    transform: translateY(-2px);
    border-color: rgba(102, 126, 234, 0.4);
  }
  .contribution-item .icon {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }
  .contribution-item h4 {
    margin-top: 0;
    font-size: 0.95rem;
    font-weight: 600;
  }
  .contribution-item p {
    font-size: 0.88rem;
    opacity: 0.8;
    margin-bottom: 0;
  }
  .algo-box {
    border-left: 4px solid #764ba2;
    padding: 1rem 1.5rem;
    margin: 1rem 0;
    background: rgba(118, 75, 162, 0.04);
    border-radius: 0 8px 8px 0;
  }
  .algo-box h4 {
    color: #764ba2;
    margin-top: 0;
  }
  .assumption-tag {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 15px;
    font-size: 0.8rem;
    font-weight: 500;
    margin: 2px 4px 2px 0;
  }
  .assumption-tag.required {
    background: rgba(245, 87, 108, 0.1);
    color: #f5576c;
    border: 1px solid rgba(245, 87, 108, 0.3);
  }
  .assumption-tag.proven {
    background: rgba(79, 172, 254, 0.1);
    color: #4facfe;
    border: 1px solid rgba(79, 172, 254, 0.3);
  }
  .section-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
    margin: 2rem 0;
  }
---

<div class="hero-section">
  <span class="venue">ICLR 2026</span>
  <h2>Published as a Conference Paper</h2>
  <div class="authors">
    Arshia Soltani Moakhar, Tanapoom Laoaron, Faraz Ghahremani, Kiarash Banihashem, MohammadTaghi Hajiaghayi
  </div>
  <div class="affiliation">University of Maryland</div>
</div>

## Abstract

This paper advances the theoretical understanding of **active learning label complexity** for decision trees as binary classifiers. We provide the first analysis of the **disagreement coefficient** for decision trees and present the first general active learning algorithm that achieves a **multiplicative error guarantee**, producing a $$(1 + \epsilon)$$-approximate classifier. By combining these results, we design an active learning algorithm for decision trees that uses only a **polylogarithmic number of label queries** in the dataset size.

<hr class="section-divider">

## Key Contributions

<div class="contribution-grid">
  <div class="contribution-item">
    <div class="icon">&#127919;</div>
    <h4>Multiplicative Error Algorithm</h4>
    <p>First active learning algorithm for classification that achieves a (1+&epsilon;)-multiplicative error guarantee, stronger than traditional additive models.</p>
  </div>
  <div class="contribution-item">
    <div class="icon">&#127795;</div>
    <h4>Decision Tree Label Complexity</h4>
    <p>First label complexity bound for active decision tree learning: polylogarithmic in dataset size under natural assumptions.</p>
  </div>
  <div class="contribution-item">
    <div class="icon">&#128290;</div>
    <h4>Disagreement Coefficient Analysis</h4>
    <p>First explicit bound on the disagreement coefficient for decision trees: &theta; = O(ln<sup>d</sup>(n)).</p>
  </div>
  <div class="contribution-item">
    <div class="icon">&#128271;</div>
    <h4>Necessity of Assumptions</h4>
    <p>Proved that both structural assumptions are necessary: relaxing either leads to polynomial label complexity.</p>
  </div>
</div>

<hr class="section-divider">

## Main Results

<div class="result-card">
  <span class="theorem-label">Theorem 1.1 &mdash; Disagreement Coefficient</span>
  <p>
    For a decision tree classification task over a dataset of <em>n</em> points where each node tests a distinct feature dimension and tree height is at most <em>d</em>, the disagreement coefficient satisfies:
  </p>

  $$\theta = O\!\left(\ln^d(n)\right)$$

  <p>with a matching lower bound of &Omega;(c(ln(n) - c')<sup>d-1</sup>).</p>
</div>

<div class="result-card">
  <span class="theorem-label">Theorem 1.2 &mdash; Multiplicative Error Algorithm</span>
  <p>
    Algorithm 2 returns a (1 + &epsilon;)-approximate classifier with probability &gt; 1 - &delta; using:
  </p>

  $$O\!\left(\ln(n)\theta^2\!\left(V_H \ln \theta + \ln \frac{\ln n}{\delta}\right) + \frac{\theta^2}{\epsilon^2}\!\left(V_H \ln \frac{\theta}{\epsilon} + \ln \frac{1}{\delta}\right)\right)$$

  <p>queries, where <em>V<sub>H</sub></em> is the VC dimension and &theta; is the disagreement coefficient.</p>
</div>

<div class="result-card">
  <span class="theorem-label">Corollary 1.3 &mdash; Decision Tree Label Complexity</span>
  <p>
    Combining the disagreement coefficient bound with the multiplicative error algorithm, the total number of label queries is:
  </p>

  $$O\!\left(\ln^{2d+2}(n)\!\left(2^d(d + \ln \text{dim})d + \ln \frac{1}{\delta}\right) + \frac{\ln^{2d}(n)}{\epsilon^2}\!\left(2^d(d + \text{dim}) \ln \frac{\ln^d(n)}{\epsilon} + \ln \frac{1}{\delta}\right)\right)$$

  <p>which is <strong>polylogarithmic</strong> in <em>n</em>.</p>
</div>

<hr class="section-divider">

## Why Multiplicative Error Matters

A key insight of this work is that **additive error algorithms cannot be adapted** for multiplicative settings. The natural idea of setting $$\epsilon_{\text{additive}} = \epsilon \cdot \eta$$ (where $$\eta$$ is the optimal error) fails because estimating $$\eta$$ itself requires $$\Omega(1/\eta)$$ labels, making the label complexity dependent on an unknown, potentially very small quantity.

Our approach is fundamentally different: the algorithm is **agnostic to the magnitude of the optimal error**. It exploits the fact that when the version space fails to shrink rapidly, this signals high error, which makes $$(1+\epsilon)$$-approximation easier.

<hr class="section-divider">

## Algorithm Overview

<div class="algo-box">
  <h4>Algorithm 1: Decision Stump (1D warmup)</h4>
  <p>
    Maintains an interval [L, R] of candidate stumps. Each iteration <strong>samples</strong> labels, <strong>bounds</strong> errors, and <strong>prunes</strong> provably suboptimal classifiers. If the interval fails to halve, the algorithm switches to a <strong>direct estimation phase</strong> using O(1/&epsilon;<sup>2</sup>) additional samples. This two-regime approach is the key innovation.
  </p>
</div>

<div class="algo-box">
  <h4>Algorithm 2: General Binary Classification</h4>
  <p>
    Generalizes the stump algorithm by replacing intervals with hypothesis sets H<sub>i</sub>, sampling from the <strong>disagreement region</strong> DIS(H<sub>i</sub>), and tracking progress via the <strong>radius</strong> of the hypothesis set. The disagreement coefficient &theta; bridges the gap between hypothesis ball radius and disagreement region size.
  </p>
</div>

<div class="row">
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/active-learning-dt/decision_tree.png" title="Decision Tree" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/active-learning-dt/Line_tree.png" title="Line Tree" class="img-fluid rounded z-depth-1" zoomable=true %}
    </div>
</div>
<div class="caption">
    (Left) A decision tree with 4 leaves (L = 4). Leaf 1 uses dimensions 1, 2. (Right) LineTree<sub>h,3</sub> classifies all samples as 1 − l<sub>h,3</sub> except those reaching leaf 3 of h.
</div>

<hr class="section-divider">

## Structural Assumptions & Their Necessity

<p>
  <span class="assumption-tag required">Required</span>
  <strong>Unique dimensions per path:</strong> Each node on a root-to-leaf path must test a feature dimension distinct from its ancestors.
</p>
<p>
  <span class="assumption-tag required">Required</span>
  <strong>Grid-like data structure:</strong> Input data lies on a regular grid X = {(a<sub>1</sub>, ..., a<sub>dim</sub>) | a<sub>i</sub> &isin; N, a<sub>i</sub> &le; w}.
</p>

<p>
  <span class="assumption-tag proven">Proven necessary</span>
  Without the unique dimension constraint, &theta; = &Omega;(n<sup>1/dim</sup>) &mdash; polynomial, not polylogarithmic.
</p>
<p>
  <span class="assumption-tag proven">Proven necessary</span>
  Without grid structure (e.g., data on a line), &theta; = &Omega;(n) even with unique dimensions per path.
</p>

The uniformity assumption can be partially relaxed by assigning weights $$W_i \in [1, \lambda]$$ to each data point, which scales the disagreement coefficient by at most $$\lambda^2$$.

<hr class="section-divider">

## Lower Bound

<div class="result-card">
  <span class="theorem-label">Theorem 4.3 &mdash; Label Complexity Lower Bound</span>
  <p>
    Any active learning algorithm requires at least:
  </p>

  $$\Omega\!\left(\ln\!\left(\frac{1}{\delta}\right) \cdot \frac{1}{\epsilon^2}\right)$$

  <p>queries to return a (1 + &epsilon;)-approximate decision stump with probability > 1 - &delta;. This shows our algorithm's dependence on &epsilon; is close to optimal (up to logarithmic factors).</p>
</div>

<hr class="section-divider">

## Acknowledgments

This work is partially supported by DARPA expMath, ONR MURI 2024 award on Algorithms, Learning, and Game Theory, Army-Research Laboratory (ARL) grant W911NF2410052, NSF AF:Small grants 2218678, 2114269, 2347322.
