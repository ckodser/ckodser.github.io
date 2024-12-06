---
layout: post
title: Interpretability Beyond Feature Attribution  Quantitative Testing with Concept Activation Vectors (TCAV)
tags: Interpretability
date: 2024-11-02 15:09:00
description: summary of Interpretability Beyond Feature Attribution  Quantitative Testing with Concept Activation Vectors (TCAV)
categories: Summary
thumbnail: assets/Interpretability_Beyond_Feature_Attribution_Quantitative_Testing_with_Concept_Activation_Vectors_(TCAV)/image9.png
featured: true
---
[1711.11279] Interpretability Beyond Feature Attribution: Quantitative Testing with Concept Activation Vectors (TCAV)
The concept should come from the user side. Each concept is defined by several images, like stipe images. Then they used a bottle neck (m) in the model and train a linear classifier between these provided images and random images. Then they can measure the influence of a concept on an image from a model's perspective. they calculate gradient of the image and backprop till the bottle neck and multiply it with the learned classifier. 
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.html path='assets\img\Interpretability_Beyond_Feature_Attribution_Quantitative_Testing_with_Concept_Activation_Vectors_(TCAV)\image9.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
They offer a relative TCAV that gets multiple concepts and learns the classifier to distinguish between these concepts (no random sample anymore). This will help us to detect the relationship between concepts. For example we can learn dot <-> stripe classification and check how much a zebra has one of them. 
