---
layout: page
title: BasedOn
description: Using Learnable If Statements for Interpretability
img: assets/img/basedOn/Code.png
importance: 1
giscus_comments: true
category: Interpretability
---

When You have a program, and you want to use AI init, you usually don't want to rewrite the program from scratch again.
You want to out-source some decision makings to AI and maintain your source code structure.
Current machine learning libraries, however, do not let you do that. If you want to use them you should rewrite everything around them.

In this paper we introduce BasedOn. A library that let you have learnable If statements. You write your If Statement and arguments that its decision should be based. The code will automatically learn that if statement in such a way that maximized the reward.
BasedOn uses RL techniques under the hood hence reward could be non-differentiable, allowing maximum flexibility.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/basedOn/img1.png" title="SPADE" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    (a): Car decision-making function using BasedOn. Valley is the x value of valley
threshold. (b): MountainCar-V0 visualized state. (c): average reward of the algorithm presented
in part (a) compared to vanilla policy gradient, showing the usefulness of programmer intuition.
Models were trained on 500 episodes each for 1000 steps. Mean and standard deviation are averaged
across 20 runs.
</div>
you can read more from the paper [OpenReview](https://openreview.net/pdf?id=gyl8r8ANcd).
