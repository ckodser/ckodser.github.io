---
layout: page
title: A Mathematical Framework for Transformer Circuits
description: In Transformers residual stream is the main object and layers read and write from/to it.
categories: [Summary, Interpretability]
img: assets/img/A_Mathematical_Framework_for_Transformer_Circuits/img_3.png
importance: 1
giscus_comments: true
link: https://transformer-circuits.pub/2021/framework/index.html
---

<h1> One Layer Transformers </h1>
One layer transformers (without MLP) are combinations of $$a$$->$$b$$ and {$$a$$, …, $$b$$} -> $$c$$.
this is because they either don’t use the attention head which means the score is calculated by a.Encoding.Decoding, or the path uses attention head which means attention head on token $$b$$ attend to token $$a$$ and if it attends then token $$c$$'s probability is raised.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/A_Mathematical_Framework_for_Transformer_Circuits/img_1.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

<h1> Induction Heads</h1>
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/A_Mathematical_Framework_for_Transformer_Circuits/img_2.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

Induction Heads find similar text to the current suffix in the previous text and raise the probability of the next token. For example if in the text we have many "Mr Dursley" and your current suffix is "Mr Du", then the model attends to "rsley" in the previous tokens and correctly predicts "rsley".

But How Induction Heads works?
Their trick is that one of the attention heads key is the previous token info, meaning the key is the shifted value of tokens. The Query value if current token info. This way if two location matches (have same value) since the key is shifted, then the info of "rsley" moves to the last token.
