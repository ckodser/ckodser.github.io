---
layout: page
title: An Overview of Early Vision in InceptionV1
description: inceptionV1 feature maps of different layers
categories: Interpretability
img: assets/img/An_Overview_of_Early_Vision_in_InceptionV1/image5.png 
importance: 1
link: https://distill.pub/2020/circuits/early-vision/
---



first layer of inceptionV1 has three groups of neurons.
Gabor filters are like edge detectors. but each of them could only detect edges at a specific angle. 
Color Contrast filters will be activated if they see one color in one side of their field of view and another color in another side. 
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/An_Overview_of_Early_Vision_in_InceptionV1/image5.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
Second layer has many groups. 
<div class="row">
        <div class="col-sm mt-3 mt-md-0">
            {% include figure.liquid path='assets/img/An_Overview_of_Early_Vision_in_InceptionV1/image4.png' class="img-fluid rounded z-depth-1" %}
        </div>
    </div>
it gets more and more complex as we go deeper. 
