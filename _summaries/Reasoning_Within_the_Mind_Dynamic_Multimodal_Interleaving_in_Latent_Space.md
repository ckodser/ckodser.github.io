---
layout: page
title: Reasoning Within the Mind Dynamic Multimodal Interleaving in Latent Space
description: Training free latent reasoning. Optimize the latent reasoning tokens to maximize the model confidence which is correlated with the model accuracy.
categories: [Reasoning]
img: assets/img/Reasoning_Within_the_Mind_Dynamic_Multimodal_Interleaving_in_Latent_Space/image1.png
importance: 1
giscus_comments: true
link: https://arxiv.org/pdf/2512.12623
---

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Reasoning_Within_the_Mind_Dynamic_Multimodal_Interleaving_in_Latent_Space/image1.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

To measure if a token depend on the image they make the image noisy and measure if the probability of that token drops.

$$S_{i,t} = \log \pi_{\theta}(x_{i,t} \mid x_{i,<t}, I, q) - \log \pi_{\theta}(x_{i,t} \mid x_{i,<t}, \tilde{I}, q)$$

They show that

1) only a small subset of tokens really depend on the image.

2) reasoning sequences that depends more on the image have higher accuracy.


<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Reasoning_Within_the_Mind_Dynamic_Multimodal_Interleaving_in_Latent_Space/image2.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>



They make these additional observations.

1) Higher Confidence Tends to Indicate Higher Reasoning Accuracy.

2) onfidence Reflects Reasoning Chains Quality.

3) High Confidence Aligns with Stronger Visual Grounding.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Reasoning_Within_the_Mind_Dynamic_Multimodal_Interleaving_in_Latent_Space/image3.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

# Method

Their method is training free. But in the inference they have an optimization which might be heavy. They add $$L$$ latent tokens to the first of generation and try to update their embeddings so that everything works better. So the input sequence became

$$[\text{Image embeddings}, \text{question embeddings}, V_{best}, L_1,L_2,\cdots, L_L]$$

But the embeddings of the $$L$$ latent tokens are learn in such a way that the confidence of the model get maximize. So they try to optimize $$L_i$$ embeddings such that the model confidence is maximized. They measure the model confidence using:


$$H_k(P_i^{(t)}) = - \sum_{w \in \text{Top}_k(P_i^{(t)})} P_i^{(t)}(w) \log(P_i^{(t)}(w))$$

$$R(T^{(t)}) = 1 - \frac{1}{L} \sum_{i=1}^{L} H_k(P_i^{(t)})$$


So the more confidence the model the better. They do the latent optmization and image patch selection $$T$$ times. Then decode using those two.

## Optimization of latent embeddings

They used REINFORCE-based optimization.

$$T^{(t)} \leftarrow T^{(t)} + \eta \nabla_{T^{(t)}} J(T^{(t)})$$

where


$$\nabla_T J(T) = \mathbb{E}_{T' \sim \pi(\cdot\lvert T)} [R(T') \nabla_T \log \pi(T' \rvert T)] = \mathbb{E}[R(T') \frac{\epsilon}{\sigma^2}]$$

and

$$T'^{(t)} = T^{(t)} + \epsilon^{(t)}, \quad \epsilon^{(t)} \sim \mathcal{N}(0, \sigma^2 I)$$


## Optimization of $$V_{best}$$

move on latent tokens 1 by 1. find the top $$m$$ visual tokens it attend to (based on the attentino pattern). Add those to the $$V_{best}$$. Check if the reward increases. If it does update the $$V_{best}$$. else don't.

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Reasoning_Within_the_Mind_Dynamic_Multimodal_Interleaving_in_Latent_Space/image4.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
