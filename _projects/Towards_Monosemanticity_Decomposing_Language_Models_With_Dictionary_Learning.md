---
layout: post
title: Towards Monosemanticity Decomposing Language Models With Dictionary Learning
description: summary of Towards Monosemanticity  Decomposing Language Models With Dictionary Learning
categories: Summary
img: assets/img/Towards_Monosemanticity_Decomposing_Language_Models_With_Dictionary_Learning/image17.png 
importance: 1
---


Towards Monosemanticity: Decomposing Language Models With Dictionary Learning
they tried to understand this network
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.html path='assets\img\Towards_Monosemanticity_Decomposing_Language_Models_With_Dictionary_Learning\image17.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
They believe our neural networks simulated a much larger, much sparser neural networks
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.html path='assets\img\Towards_Monosemanticity_Decomposing_Language_Models_With_Dictionary_Learning\image18.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
sparse autoencoder tries to reconstruct MLP activation with a one hidden layer network. So it is 
MLP activations —-(linear)-----> hidden layer (sparse features) —(linear)---> MLP activations.
They investigate 4 features. I will explain the Arabic script feature only.
Arabic script feature
When the feature is active the context is Arabic. Arabic text is quite rare in our overall data distribution –  just 0.13% of training tokens — but it makes up 81% of the tokens on which our feature is active.When the context is Arabic the feature is active (usually) This feature does not fire on words starting with ال. Another feature to this.Nevertheless, we find a Pearson correlation of 0.74 between the activity of our feature and the activity of the Arabic script proxy (thresholded at 0), over a dataset of 40 million tokens.interpretable causal effects on model outputs:activating the feature increase the chance of choosing arabic wordsThe feature is not a neuron. They looked at coefficient of the featureIt is universal. train the network with another seed -> the same feature existed. 
<h4> AUTOMATED INTERPRETABILITY – ACTIVATIONS </h4>
They Used an LLM to get many samples a feature is activated on and produce an explanation. Then using the explanation of the feature it tries to predict the feature activation on other samples. 
<h3> Feature Splitting </h3>
when they increase the number of features (hidden layer size) features split to multiple features. 
