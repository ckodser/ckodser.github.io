---
layout: page
title: Zoom In An Introduction to Circuits
description: Investigate Vision Circuits by Studying the Connections between Neurons
categories: [Summary, Interpretability]
img: assets/img/Zoom_In_An_Introduction_to_Circuits/image20.png
link: https://distill.pub/2020/circuits/zoom-in/
importance: 1
---

By studying the connections between neurons, we can find meaningful algorithms in the weights of neural networks.

Three Speculative Claims about Neural Networks <br>

1. **Claim 1: Features**
   Features are the fundamental unit of neural networks.
   They correspond to directions. 1 These features can be rigorously studied and understood.
2. **Claim 2: Circuits**
   Features are connected by weights, forming circuits. 2
   These circuits can also be rigorously studied and understood.
3. **Claim 3: Universality**
   Analogous features and circuits form across models and tasks.

To support Claim 1 (features) they suggest there are some neurons corresponding to curves (around 60 pixels and at a
specific angle) like below. There are some related shapes that use curves but do not count as one.
<h3> Understanding Features </h3>
<h4> curves </h4>
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Zoom_In_An_Introduction_to_Circuits/image20.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
How are they sure that these neurons do curve detection?
1. feature visualization, dataset examples, synthetic examples
2.when rotating a sample, curve detections stop firing and curve detections corresponding to the next angle starts firing
3. looking at weights suggests they detect curves

<div class="col-sm mt-3 mt-md-0">
   {% include figure.liquid path='assets/img/Zoom_In_An_Introduction_to_Circuits/image1.png' class="img-fluid rounded z-depth-1" %}
</div>

4. next layers features that uses these needs curves (like circle need curves)
5. make these circuits by hand (setting weights) and the behavior is very similar to the neurons.


<h4> High-Low Frequency Detectors </h4>
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Zoom_In_An_Introduction_to_Circuits/image19.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
these features detect high frequency in one side and low frequency in the other side probably to detect edges and background (out of focus and low frequency) from foreground (high frequency)
<h4> Dog feature  </h4>
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Zoom_In_An_Introduction_to_Circuits/image21.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
Detects dogs from any angle. used feature vis and dataset samples to prove.
<h3> Understanding Circuits </h3>
<h4> curves </h4>
earlier curves which are smaller act as tangents of the longer curves. Same sided curves boost the curves in the next layer, and opposite sided curves inhibited next layer curve detectors.
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Zoom_In_An_Introduction_to_Circuits/image25.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
<h4> Dog detectors </h4>
There are two separate paths in inception for detecting dog heads. The first one detects left oriented heads, while the second one detects right oriented heads. 
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Zoom_In_An_Introduction_to_Circuits/image23.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
Then by combining them, the network detects heads in any pose. 
<h4> car detection </h4>
the same story here, car is composed of car wheels, windows, car body. 
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Zoom_In_An_Introduction_to_Circuits/image15.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
But after this some interesting things happen. The network decides to move the car to superposition. 
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/Zoom_In_An_Introduction_to_Circuits/image2.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
