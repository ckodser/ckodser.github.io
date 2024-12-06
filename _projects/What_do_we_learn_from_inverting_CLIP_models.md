---
layout: post
title: What do we learn from inverting CLIP models?
description: summary of What do we learn from inverting CLIP models?
categories: Summary
img: assets/img/What_do_we_learn_from_inverting_CLIP_models/image16.png 
importance: 1
---


https://arxiv.org/pdf/2403.02580v1
how to use CLIP as a text to image? 
by doing this optimization:
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.html path='assets\img\What_do_we_learn_from_inverting_CLIP_models\image16.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
V is the vision part of CLIP, T is the test part of CLIP, A(x) is a random augmentation of x and Reg(x) is a regularization of x. 
