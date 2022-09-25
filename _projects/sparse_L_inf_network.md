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

As shown above, neurons calculate L-inf distance only in some dimensions and other dimensions ignored, each dimension is an edge in the above graph.
Which means we remove 98% of edges, without any accuracy, certified accuracy decrease.

the approch which we choose edges to remove was very simple. Using training dataset we count in how many samples an spesific edge cause the L-inf distance change. L-inf distance could be seen as a max function on absolute values. Mathematically\
$$\| W \| = max(\|W_i\|)$$\
So in each Maximum we checked which element matters. After this calculation we remove edges which counted less than a specific constant.


This work raise an interesting questions, if this network doesn't use its full capacity, what happens if it does? It is an important question since it is proved that robustness need more parameter and if our network doesn't use its full capacity it somehow means it has fewer parameters.
to mitigate this issue I purposed median-neuron which calculate\
$$y=median(X_i-W_i)+b$$ instead of $$y=max(\|X_i-W_i\|)$$\
At first it seems, this neuron could get higher accuracy and robust accuracy since median is a robust function by its nature. Nevertheless, we were not able to train this network properly.

In addition to median we tried r-th element in the sorted array function. It means each neuron has a learnable $$R$$ and its output calculated as follows\
$$y=(Sorted(X_i-W_i)_R)+b$$ to make these $$R$$s learnable, we should apply some normalization to R-th element function; Therefore during training we applied 
$$y=\sum_{i} {Sorted(X_j-W_j)_i}^T(R-i)$$\Which T is an increasing function. 

codes are in [Github](https://github.com/ckodser/L_inf_dist_mean).