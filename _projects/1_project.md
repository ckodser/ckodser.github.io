---
layout: page
title: Certified Robust Neural Network
description: Certify Robustness using median neurons
img: assets/img/inf-neuron.png
importance: 1
category: Robustness
---
L-inf dist neurons are introduced by , [zhang2021towards](https://github.com/zbh2047/L_inf-dist-net). With this neuron they have achieved supiriour certified accuracy on various datasets including CIFAR-10.  
<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/inf-neuron.png" title="L-Inf distance neuron" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    This illustration shows how an L-inf distance neuron works.
</div>

As shown in the illustration, each neuron calculated L-inf dist of its input to some learnable point, plus a fix constant. With this formulation Lipschitz of each neuron output with respect to its input is $1$; Therefore each layers Lipschitz is equal to $1$ and further the whole network is Lipschitz one. Lipschitz's networks could easily certify their robustness under L-inf perturbations.\
In the first experiment I Found out this network could sparsified with 98% puring ratio without losing accuracy or certified accuracy.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/sparseNeuron.png" title="sparsed L-Inf distance neuron" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    This illustration shows how an L-inf distance neuron sparsified. 
</div>