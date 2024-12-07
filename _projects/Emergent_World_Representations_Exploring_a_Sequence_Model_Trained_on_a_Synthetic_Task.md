---
layout: post
title: Emergent World Representations Exploring a Sequence Model Trained on a Synthetic Task
description: summary of Emergent World Representations  Exploring a Sequence Model Trained on a Synthetic Task
categories: Summary
img: assets/img/Emergent_World_Representations_Exploring_a_Sequence_Model_Trained_on_a_Synthetic_Task/image11.png 
importance: 1
---


https://arxiv.org/abs/2210.13382
Task is comming up with valid othello board moves. Predict othello board state from hidden state activations. State of each cell is empty & black & white. linear prob doesn’t work but one layer MLP leads to 98% accuracy. 
lets change worldstate manually and see if predictions match our changes. To do this they first change the world model from top five layers like the image below.
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets\img\Emergent_World_Representations_Exploring_a_Sequence_Model_Trained_on_a_Synthetic_Task\image11.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
how to intervene in one worldmodel, using only the probing model that predicts the worldmodel?
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets\img\Emergent_World_Representations_Exploring_a_Sequence_Model_Trained_on_a_Synthetic_Task\image24.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
They applied SGD to the activations in a way that the color changes to the other color. 
After this, the model is giving the answer of the altered worldmodel with a very high accuracy which means this worldmodel is causal to the model prediction and the model Uses this worldmodel for its prediction. 
<h3> latent saliency maps </h3>
They measure how much each cell affects the probability of a prediction. red->important, black square -> destination. For each cell they intervene it and measure the change in the probability. 
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets\img\Emergent_World_Representations_Exploring_a_Sequence_Model_Trained_on_a_Synthetic_Task\image3.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
