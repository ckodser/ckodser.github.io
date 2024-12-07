---
layout: page
title: A Mathematical Framework for Transformer Circuits
description: summary of A Mathematical Framework for Transformer Circuits
categories: Summary
img: assets/img/faviconDALLE.ico 
importance: 1
---


A Mathematical Framework for Transformer Circuits
One layer transformers (without MLP) are combinations of a->b and c, …, a -> b.
this is because they either don’t use the attention head which means the score is calculated by a.Encoding.Decoding, or the path uses attention head which means attention head on token a attend to token c and if it attends token b probability is raised. 
