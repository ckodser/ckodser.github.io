---
layout: page
title: DASH Detection and Assessment of Systematic Hallucinations of VLMs
description: Make a dataset that VLMs hallucinate and wrongly think things exist in images 
categories: Hallucination
img: assets/img/DASH_Detection_and_Assessment_of_Systematic_Hallucinations_of_VLMs.png 
importance: 1
giscus_comments: true
link: https://arxiv.org/abs/2503.23573
---

In this paper they build a dataset that makes VLMs Hallucinate. They used two approaches  DASH-LLM, DASH-OPT.

## DASH-LLM

An LLM is asked to generate 50 prompts that leads a VLM to hallucinate something without mentioning the object itself.
For example with `object: dining table` the LLM generates this prompt. 
> *A charming café interior with ceramic cups and saucers on individual stands.*


These generated text queries `(qtext)` then serve as input for the exploration phase. For each query, a k-NN retrieval (using CLIP similarity) is performed on the massive ReLAION-5B image dataset to find semantically similar real-world images.

Then they filtered the retrieved images based on these two filters.
1) An open-world object detector (OWLv2) is used to verify that the target object is not actually present in the retrieved images. Images where the detector confidently identifies the object are discarded. 
2) The target VLM is then queried (e.g., "Can you see a [object] in this image?"). Only images where the VLM incorrectly responds "Yes" (hallucinates) are kept.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path='assets/img/DASH_Detection_and_Assessment_of_Systematic_Hallucinations_of_VLMs3.png' class="img-fluid rounded z-depth-1" %}
    </div>
</div>

## DASH-OPT

Tey try to optimize $$c$$ which is a embeddings that using that one-step diffusion generates an image. 
They try to optimize this 

$$min_c (L_\text{vlm}(c) + L_\text{det}(c))$$

where $$L_\text{vlm}(c)$$ measures howmuch the generated object mislead the vlm (it thinks it contains [object]) and $$L_\text{det}(c)$$ measures how much that image really has that [object]. So the goal is that VLM thinks there is an [object] in the image but object detection method here OWL thinks there is no object. 

In more detail, $$q(c)$$ is the function that generates images from the embedding. 
we have:

$$L_{vlm}(c) = - \log p_{vlm}(\text{"Yes"} | q(c), \text{Is there [object] in this image?})$$

and 

$$L_{det}(c) = - \log (1 - p_{det}([object] | q(c)))$$

the final image is called  `(qimg)` and then they apply the normal knn search and filtering. 
So they find 50 similar images in LAION-5B and then filtered images with the [object] or those that LLM doesn't hallucinate.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path='assets/img/DASH_Detection_and_Assessment_of_Systematic_Hallucinations_of_VLMs4.png' class="img-fluid rounded z-depth-1" %}
    </div>
</div>

First image of each row is a random image from the class and the second image is the generated image by DASH-OPT and the rest are the retrieved images.


