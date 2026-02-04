---
layout: page
title: Progress measures for grokking via mechanistic interpretability
description: summary of Progress measures for grokking via mechanistic interpretability
categories: [Summary]
img: assets/img/faviconDALLE.ico
importance: 2
---


https://arxiv.org/abs/2301.05217
A simple network which gets ab= and learns to output (a+b)%p will do a weird thing. It first maps a, b to sin(ka), cos(ka), sin(kb), cos(kb) for several k values using a simple embedding matrix.  in the attention and MLP inputs it calculates sin and cos of (a+b). Using output of MLP neurons and unembed which together forms a n->p linear projection it calculates logit_c=sum(cos(k(a+b-c))) for many k. if c=a+b then for any k this value is 1 and logit is large.  
How do they prove their network is doing this?
fourier components of matrices. (hard shit)The second part is easy to check from weights if we know k values for each neuron in MLP. Since each neuron is calculating either sin(k(a+b)) or cos(k(a+b)) the connection to logit c is calculable. In the first case, the connection should be sin(kc) and in the later one it should be cos(kc)They replace neurons by what they think each neuron should do and the performance improved or remained unchanged. activations are periodic
So what?
They used this technique to show that neural network training has three phases 1. memorization, 2. generalization and 3. cleaning.
