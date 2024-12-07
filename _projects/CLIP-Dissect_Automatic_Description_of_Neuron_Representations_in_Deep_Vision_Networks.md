---
layout: post
title: CLIPDissect Automatic Description of Neuron Representations in Deep Vision Networks
description: summary of CLIP-Dissect  Automatic Description of Neuron Representations in Deep Vision Networks
categories: Summary
img: assets/img/CLIP-Dissect_Automatic_Description_of_Neuron_Representations_in_Deep_Vision_Networks/image13.png 
importance: 1
---


[2204.10965] CLIP-Dissect: Automatic Description of Neuron Representations in Deep Vision Networks
Their algorithm has three steps. In the first step using a clip model, an image dataset, and a concept set, they do the
following. for each pair of concept and image they calculate their similarity (easy with CLIP). They just first compute
embeddings for each concept and image and use dot products to compute similarity.
In the second step, if we have a single neuron in mind they compute the neuron activation on the whole dataset. if
neuron k is chosen, A_k(x_i) refers to the activation map of this neuron on sample i. g acts like an average poll.
in the last step they find the most similar column in the table P and return that concept as the neuron functionality.
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets\img\CLIP-Dissect_Automatic_Description_of_Neuron_Representations_in_Deep_Vision_Networks\image13.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
Interesting thing is that while all concepts should be in the concept set, even if those concepts are missing from the imageset, they might be able to return those concepts. probably because CLIP is great.
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets\img\CLIP-Dissect_Automatic_Description_of_Neuron_Representations_in_Deep_Vision_Networks\image6.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
