---
layout: page
title: Physics of Language Models
description: Understanding LLMs by training smaller LMs in controlled environment
categories: [Summary, Interpretability]
img: assets/img/Physics_of_Language_Models/Physics_of_Language_Models_main.png
importance: 1
giscus_comments: true
link: https://physics.allen-zhu.com/home
---

# Part 1

They trained a model on a synthetic grammar. 

like 
```
S -> AB
S -> BA
A -> 12
B -> 31
```

This is an actual example:
<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path='assets/img/Physics_of_Language_Models/Physics_of_Language_Models_0.png' class="img-fluid rounded z-depth-1" %}
    </div>
</div>

They trained an LM on this and showed the model has good accuracy/diversity/everything. 
Then they showed that when the model is probed, it has the knowledge of related dp states that we use to calculate and see if the string belongs to that language. By DP states, I mean the state that we are in the middle of which upper layer variable. 
It also stores if the upper layer variable is finished. 

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path='assets/img/Physics_of_Language_Models/Physics_of_Language_Models_half.png' class="img-fluid rounded z-depth-1" %}
    </div>
</div>

They also show that the model looks at those previous tokens that are really matter for updating these states. So it really updates its DP states properly. 

**Corrupted data**: if you want to test your model with corrupted data, you should obviously add corrupted data to its training dataset. They showed this work but with a catch. The model learns that the training data has two mode: correct and corrupt. It your inference data is too much corrupt it continues to complete it with corrupt data. 
# Part 2.1

- We need to train smaller LMs to understand them because if we didn't train an LM, we are not sure about the training data, and we can even be sure that the abilities we see are memorization or generalization.
- They build iGSM that is a synthetic GSM8K-like dataset. It has a few fixed objects that have some fixed relationships together.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path='assets/img/Physics_of_Language_Models/Physics_of_Language_Models_2.png' class="img-fluid rounded z-depth-1" %}
    </div>
</div>

- They trained a GPT-2 model which learned the data
- They defined the level of reasoning skills
  - level-0: Go in circles and check if you can calculate a variable and if you can, calculate it. 
  - level-1: uses topological sort + gives shortest CoT.
- they showed GPT does level-1 reasoning -> it never computes unnecessary variables. 
- How does the model know what variables are important before start answering? Using probing, they showed these: 
    - the model knows what variables are required for answering the question, (right after the question finishes)
    - In the solution, it knows what variables can be computed next (their dependencies are calculated already)
    - Before the question, the model knows whether variable A depends on variable B, for all A and B. 
      - Unlike humans, it doesn't track back from the question. It keeps its knowledge updated after each new sentence.
- They showed that **Depth matters for reasoning**: The accuracy depends on dept more that on its width.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path='assets/img/Physics_of_Language_Models/Physics_of_Language_Models_3.png' class="img-fluid rounded z-depth-1" %}
    </div>
</div>

- Only **Deeper layers** can be probed so that we get a high accuracy on "whether variable A is necessary for computing the answer."


## How they probed?

When they wanted to know what knowledge the model has about a variable, they attached that variable name to the end of the sentence like the following image and then probed at that point. They trained a rank-8 update on input embedding and a trainable linear layer on the output embedding.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path='assets/img/Physics_of_Language_Models/Physics_of_Language_Models_4.png' class="img-fluid rounded z-depth-1" %}
    </div>
</div>

# Part 2.2

LLMs are not perfect in reasoning. 