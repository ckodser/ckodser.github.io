---
layout: page
title: sparsity for interpretability
description: Leveraging sample sparsity to improve interpretability of neural networks 
img: assets/img/spade/images/SPADE_method_Square_jitter.png
importance: 1
category: Interpretability
---

In this paper we improved interpretability methods by first pruning the model on the sample of interest and then apply the interpretability method. This approach let we apply global interpretability methods as a local interpretability. We showed with our experiments that this approach will improve the interpretability methods performance including feature visualization and saliency maps.

<h2> SPADE </h2>
<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/spade/images/SPADE_method_Square_jitter.png" title="SPADE" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    SPADE pipeline. 
</div>
As showed in the image, SPADE first uses augmentation to generate many similar images to the image of interest. It then prunes the network using these generated images. We used OBS and SparseGPT methods for pruning the network. Finally we apply the interpretability method to understand the network functioning on the sample of interest. In out experiments we applied Neuron Visualization techniques and Saliency Maps. 


<h2> Why SPADE works? </h2>
As we know neural networks has many non-mono semantic neurons. These neurons get activated on many unrelated concepts. This property of neural networks makes it very hard to interpret their inner-working mechanism.
When we apply SPADE we first prune the network on our specific sample. This means neurons focus on their functionality that is related to the sample and probably became mono-semantic. We show this in a toy example in the below figure. 

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/spade/images/all.png" title="SPADE on a toy model" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
   Two-dimensional example to illustrate the effect of SPADE on feature visualization. The feature visualizations are shown with green points, where blue and orange points are positive and negative samples. The SPADE Scenario 1 shows the feature visualizations obtained when the
    sample of interest is from larger positive region. Scenario 2 shows the visualizations obtained when the 
    sample of interest is drawn from the smaller region. As we see although the final neuron is poly-semantic, when we prune the network using a sample, the neuron focus on the sample of interest and forgets its other functionality which makes interpretability easier. 
</div>

<h2> SPADE Results</h2>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/spade/images/SPADE_fig1_notrojan_nospadefirst.png" title="SPADE on a toy model" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    (Left) When SPADE is applied with feature visualization it makes feature visualizations sample specific. Instead of answering what this neuron does in general we can now answer what this neuron does "in this sample". As you can see feature visualizations gives more information when SPADE is used. (Right) Image saliency maps are also have more detail.
</div>

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/spade/images/backdoored_model.png" title="SPADE on a toy model" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    We applied SPADE to a model with backdoor. The backdoor relates some emojy with some classes. When you apply feature visualization to those classes you could not see the neurons side functionality which is detecting the emoji. However with SPADE if you prune using an image with an emoji you could see the effect. In cases you prune using an image without emoji (clean image) you get a normal feature visualization.       
</div>

For code and experiment results visit [GitHub](https://github.com/IST-DASLab/SPADE/tree/main).
