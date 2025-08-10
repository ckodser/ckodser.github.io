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

- They trained a GPT-2 model which learned the data (For an example, look at the image in Part 2.2)
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

LLMs are not perfect in reasoning. Sometimes by just saying that they made a mistake somewhere, they can correct themselves. 
They tried to improve their LLM reasoning model. Using the iGSM, they found out that in that dataset the main reason an LLM returned the wrong answer was that the model tries to compute a variable that is not ready for computation. 

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path='assets/img/Physics_of_Language_Models/solution.png' class="img-fluid rounded z-depth-1" %}
    </div>
</div>

- The model sometimes knows it made a mistake 50%-70% of the time. 
- Error detection is easy. You can train a model on error-free data, and it already knows when some data is wrong. 
- You can improve reasoning using this, when the model regrets and knows it made a mistake role back and generate that step again. From 78% -> 80%. Note that beam search doesn't improve reasoning.

But it is better if the model corrects itself. To investigate this, they wanted a dataset that solutions sometimes have error, but it corrects itself later. This is an example of this dataset. 

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path='assets/img/Physics_of_Language_Models/dataset_with_error.png' class="img-fluid rounded z-depth-1" %}
    </div>
</div>

- Doesn't this encourage model to make mistake? Shouldn't we mask the labels of mistake? so that the model doesn't learn the mistake but only to correct it mistake? Answer: even with p=0.5 the accuracy of the model increases. 
- When p increases, the model doesn't make more mistakes **that much** (it actually makes more mistakes by a little bit.) with temp=0. 
- LoRA on error-free models with the new dataset with error doesn't help.
  - Full fine-tuning works if you use lots of data. 
- So Error correction is harder than Error detection. 

## data with error generation
The method that works is that you move a later step of reasoning back, and the model midway of this reasoning step should understand that it is not yet ready for this step and output the [BACK] token.
This encourages that model to not skip reasoning steps. 

## Beam search 
 
Beam search is not that good. beam search with 32 tokens increases accuracy from 78% to 79%. 

