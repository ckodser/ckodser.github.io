---
layout: page
title: Active Learning Survey
description: Active Learning for Agnostic classification
categories: ActiveLeanring
img: assets/img/active-servey/img.png 
importance: 1
link: https://web.ics.purdue.edu/~hanneke/docs/active-survey/active-survey.pdf
---


<h1>  Conceptual Themes </h1>

They used an example to explain that in active learning we are facing two different scenarios which one of them is very hard for active learning. In the hard scenario the label complexity of active learning is very high and the only thing differentiate between these two scenario is the target function. Therefore, when they report label complexity of algorithms it is usually based on properties of target function.


The example is as follows: 
Assume our data is 1D data points with binary labels and ew want to learn an interval such that the classifier assigns + to the datapoints inside the interval and - to the datapoints outside of the interval. 

They argue that if target function is all -, then it is very hard for us to find the best interval. The only info we have is that the best interval doesn't include any point we already check its label. 
So no matter how many samples we use and check their label we are not able to return the best classifier. 

<h1> Definitions </h1>

1. For any classifier $$h$$, define $$er(h) = P_{XY} ((x, y) : h(x) \neq y), called the error rate;
2. $$\nu = \inf_{h\in C} er(h)$$
3.  Algorithm $$A$$, achieves label complexity $$\Lambda$$ if, for every integer $$n \geq \Lambda(\epsilon, \delta,P_{XY} )$$, if $$h$$ is the classifier produced by running $$A$$ with budget $$n$$, then with probability at least $$1 − \delta$$, $$er(h) \leq \epsilon$$.
4. $$d = vc(C)$$
5.  Define the $$\epsilon$$-ball centered at $$h$$ as $$B_{C,P}(h, \epsilon) =
{g \in C : P(x : g(x) \neq h(x)) \leq \epsilon}$$
6. Define the region of disagreement of $$H$$ as
$$DIS(C) = {x \in X : \exists_{h,g \in C} s.t. h(x) \neq g(x)}$$
7.  define the disagreement coefficient of $$h$$ with respect to $$C$$ under $$P$$ as
$$\theta_h (r_0) = \max(\sup_{r>r_0} \frac{P(DIS(B (h, r)))}{r},  1)$$.
8. define $$\theta(r_0) = \theta_{f^*}(r_0)$$.
8. Condition 2.3. For some $$a \in [1, \infty)$$ and $$\alpha \in [0, 1]$$, for every $$h \in C$$,
$$P(x : h(x) \neq f^*(x)) \leq a (er(h) − er(f^*))^{\alpha}$$.

<h1>  Passive Learning </h1>
In noisy case we have 

Theorem 3.4. The passive learning algorithm ERM(C, .) achieves a
label complexity $\Lambda$ such that, for any distribution $$P_{XY}$$, $$\forall \epsilon, \delta \in (0, 1)$$,

$$
\Lambda(\nu + \epsilon, \delta, P_{XY}) \leq \frac{1}{\epsilon} \left( d \log \left( \theta(\nu + \epsilon) \right) + \log \left( \frac{1}{\delta} \right) \right)
$$

and for the case with $$a, \alpha$$ we have 

$$
\Lambda(\nu + \epsilon, \delta, P_{XY}) \leq a \left( \frac{1}{\epsilon} \right)^{2 - \alpha} \left( d \log \left( \theta \left( a \epsilon^{\alpha} \right) \right) + \log \left( \frac{1}{\delta} \right) \right).
$$

<h2> Lower bounds of passive learning </h2>

there exists a distribution $$P_{XY}$$ for which $$er(f^*) = \nu$$ and

$$\Lambda(\nu + \epsilon, \delta, P_{XY}) \geq \Omega\left(\frac{\nu+\epsilon}{\epsilon^2}(d+\log(1/\delta))\right)$$.

Furthermore, for $$a ,\alpha $$, and sufficiently small $\epsilon, \delta > 0$, there exists a distribution $P_{XY}$ with these values of $$a, \alpha$$, such that

$$\Lambda(\nu + \epsilon, \delta, P_{XY}) \geq \Omega\left(a\left(\frac{1}{\epsilon}\right)^{2-\alpha}(d+\log(1/\delta))\right)$$.

<h1> Lower bounds of active learning </h1>

There exists a universal constant $$q \in (0, \infty)$$ such that, if
$$|C| \geq 3$$, then for any label complexity $$\Lambda$$ achieved by an active learning
algorithm, for any $$\nu \in (0, 1/2)$$ and sufficiently small $$\epsilon, \delta > 0$$, there
exists a distribution $$P_{XY}$$ with $$er(f^*) = \nu$$ such that

$$\Lambda(\nu + \epsilon, \delta, P_{XY}) \geq q \frac{\nu^2}{\epsilon^2} (d + \log(1/\delta)).$$


Furthermore, for any $$a \in [4, \infty), \alpha \in (0, 1]$$, and sufficiently small $$\epsilon, \delta > 0$$, there exists a distribution $$P_{XY}$$ satisfying Condition 2.3 (in fact,
satisfying (2.1) or (2.2), for $\alpha < 1$ or $\alpha = 1$, respectively) with these
values of a and $\alpha$, such that

$$\Lambda(\nu + \epsilon, \delta, P_{XY}) \geq q a^2 \left( \frac{1}{\epsilon} \right)^{2 - 2\alpha} (d + \log(1/\delta)).$$

<h1> Disagreement-Based Active Learning </h1>

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/active-survey/img_1.png' class="img-fluid rounded z-depth-1" %}
        </div>
</div>

where $$U$$ is defined by 

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/active-survey/img_2.png' class="img-fluid rounded z-depth-1" %}
        </div>
</div>

They introduced RobustCAL which is similar to $$A^2$$ algorithm. It achieves this bound,

$$\Lambda(\nu + \epsilon, \delta, P_{XY}) \leq \theta(\nu + \epsilon)  \left(\frac{\nu^2}{\epsilon^2} + \log (\frac{1}{\epsilon})\right)
\left(d \log (\theta(\nu + \epsilon)) + \log(\frac{\log (\frac{1}{\delta})}{\delta})\right) $$.

or 

$$
\Lambda(\nu + \epsilon, \delta,P_{XY}) \leq
a^2 \theta \left( a \epsilon^{\alpha} \right)
\left( \frac{1}{\epsilon} \right)^{2 - 2\alpha}
\left( d \log \left( \theta \left( a \epsilon^{\alpha} \right) \right) + \log \left( \frac{\log (a/\epsilon)}{\delta} \right) \right) \log \left( \frac{1}{\epsilon} \right),
$$

Note that we have  $$\theta(r_0) \leq \frac{1}{r_0}$$.

The normal analysis of $$A^2$$ algorithm have $$\theta(\nu + \epsilon)^2$$ instead of $$\theta(\nu + \epsilon)$$ but some works shows that a very small changes in $$A^2$$ can achieve this bound.


<h1> Bounding the Disagreement Coefficient </h1>



