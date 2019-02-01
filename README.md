
## introduction
任务驱动型聊天框架。</br>
将聊天细分为多个任务，不同的任务使用不同的对话逻辑，建立以完成某个具体任务为目标的会话场景。</br>
<p align="left">
<img width="50%" src="./tmp/introduction.png" />
<br>

主要结构简介

* 输入: 文本
* NLU: 自然语义理解。理解输入文本所属领域、用户意图、提取关键信息等
* DM: 对话管理。管理对话逻辑，实现不同场景下的会话管理
* NLG: 自然语义生成。确定每轮会话后的执行动作
* 输出: 文本（与用户交互）或动作（如打电话，开灯等）

## NLU（Natural Language Understanding）
自然语义理解。
<p align="left">
<img width="50%" src="./tmp/NLU.png" />
<br>

## word&char embedding

使用两种 embedding

* word level embedding
	* 词级别emedding，使用腾讯开源词向量：https://ai.tencent.com/ailab/nlp/embedding.html
	* 基于jieba、词向量的最长匹配分词方法
* charactor level embedding
	* 字级别embedding，使用bert开源中文模型： https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip
	* 参考bert tokenization方法，增加全角、半角转换

## 支持的多轮交互对话任务

weather，phone，yes，no，chat

## DM(dialog management)
基于slot filling的对话管理系统

## 基本环境

* python 3.6
* tensorflow=1.4
* jieba=0.39
* pymongo
* numpy
* dash==0.35.1 
* dash-html-components==0.13.4 
* dash-core-components==0.42.1  
* dash-table==3.1.11
* gunicorn==19.9.0
