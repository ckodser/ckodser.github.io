---
layout: post
title: Labeling Neural Representations with Inverse Recognition
description: summary of Labeling Neural Representations with Inverse Recognition
categories: Interpretability
img: assets/Labeling_Neural_Representations_with_Inverse_Recognition/image12.png
importance: 1
---
https://arxiv.org/abs/2311.13594
have a large dataset that each sample has some known concepts. For each neuron, find the concept that its AUC is higher if the label is that concept. report that concept as the neuron functionality. 
used Imagenet dataset. Each sample has many concepts and also add hyper concepts from worldnet to it (.e.g. dataset has dog breeds and dog is a hyper class)
They also used some logic formula (AND, OR, NOT)  to expand their concept base. Concept of a neuron could be (DOG AND NOT CAT) OR HOUSE. 
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.html path='assets\img\Labeling_Neural_Representations_with_Inverse_Recognition\image12.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
