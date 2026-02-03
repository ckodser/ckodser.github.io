---
title: LLM Latent Reasoning as Chain of Superposition
description: Train an encoder that summarizes the reasoning chunks. Then train a latent reasoing model on the summarizations it produced from some CoT data. 
categories: [latent reasoning]
link: https://arxiv.org/pdf/2510.15522
---

They first want to train an encoder that summarizes the reasoning till a checkpoint. They call it `enc`. 

Assume we have question $X$ and a reasoing chain that we split into some chunks $S_i$. So the whole thing look like this $[X,S_0,S_1,\cdots,S_N, Ans]$. The encoder should get the input 
$[X,S_0,S_1,\cdots,S_i,L]$ and produce a summary we name $Z_i$. This $Z_i$ should have this property that we can replace that chunks with $Z_i$ and the `LLM` can still continue the reasoning chain. So the LLM should be able to produce $[S_{i+1}, S_{i+2}, \cdots, S_n, Ans]$ given the $[X, Z_0, Z_1, \cdots, Z_i]$. This is considered a good summary. 

They first argue that these $Z_i$s should lie in the linear space of the input token embeddings. Since the `LLM` only know how to interpret that space. (Section 3). SO they designed `enc` to produce logits normaly given the $[X,S_0,S_1,\cdots,S_i,L]$ and then the $Z_i$ is the linear combination of the predicted tokens. 

# Training the enc and LLM models

To train these models they use the following loss: $$\ell_{\text{sup}} = \frac{1}{N} \sum_{i=1}^{N} \frac{1}{|J_i|} \sum_{t \in J_i} (-\log p_{\theta}(x_t | \mathcal{I}_i; \text{LTSuM}))$$. 

$J_i$ is the set of index of tokens in chunk $i$. $N$ is the total number of chunks. and $p_{\theta_{LLM}}(x_t | \mathcal{I}_i; \text{LTSuM}))$ is the probability that models gives the correct token $x_t$ given the previous summarise.  $[X, z_0, z_1, \cdots, z_i]$. So it measures how well the model predicts the future tokens given $Z_i$-s. Note that i this phase the model is not given the previous chunks actual text, but only the summary. 

However $\theta_{enc}$ is used to generate $Z_i$s given the previous context. So to generate $L_i$ the model sees $X, S_0, \cdots, S_i$, but not any $L_i$. 

So $In the above loss we have two different models `enc` and `LLM` involved but they have seperate cahce and everything. The only way `enc` effects that loss it trough $Z_i$s. 

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/LLM_Latent_Reasoning_as_Chain_of_Superposition/image2.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

# Training a latent reasoning model using $Z_i$s


They then use `enc` to compress/translate some CoT data (problem + reasoning + answer) to $[X, Z_0, \cdots, Z_N, Ans]$ format. They also save the $\alpha_i$ that generated those $Z_i$. These $\alpha_i$ will be used as the target of the latent reasoning model. 


The way they trained the model is that they used normal SFT loss for explicit part and some other loss for latent part. 

$$L_{\text{auto}}(\theta_{\text{llm}}) = 
L_{exp}(\theta_{\text{llm}}) + L_{lat}(\theta_{\text{llm}}).$$ 

We have 

$$L_{exp}(\theta_{\text{llm}}) = \frac{1}{|S_{\text{exp}}|} \sum_{t \in S_{\text{exp}}} (-\log q_t[y_t])$$

This is normal SFT on normal data. 

For latent part they add some noise to $\alpha_i$ like this: $\tilde{p}_t = \text{softmax} \left( \log \alpha_t + g_t \right) \quad g_t \sim \text{Gumbel}(0, 1)$.  They then do some what normal SFT on them. 

$$L_{lat}(\theta_{\text{llm}}) = \frac{1}{|S_{\text{lat}}|} \sum_{t \in S_{\text{lat}}} \mathbb{E}_{\mathbf{g}} \left[ \text{KL}(\tilde{p}_t(\mathbf{g}) \,\|\, \mathbf{q}_t) \right] $$

# Model compereses a reasoning path

In this part their figures and arguments are reasonable. They show that in the top 50 tokens in the $\alpha_i$ they have many tokens of $S_i$. They have $1.169$ on average when each chunk have two tokens, and $2.385$ on average when each chunk have 4 tokens.
So it is reasonable to assume that the model is doing the same reasoning path but faster. 
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/LLM_Latent_Reasoning_as_Chain_of_Superposition/image3.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>

# Model doing multiple reasoing path

They manually made several reasoning path for GSM8K problems. 

<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/LLM_Latent_Reasoning_as_Chain_of_Superposition/image4.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>


They measure how much the latent reasoning path intersect with these different paths and calcualte a sum like thing. They showed this value is larger than 1.7 for most samples. They try to argue this is the numbre of parallel reasoning paths the model follow. 



