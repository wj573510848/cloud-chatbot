#### 基本环境

* python 3.6
* tensorflow=1.4
* jieba=0.39
* pymongo
* numpy

#### nlu模块

1.基本领域

weather，phone，yes，no，chat

#### word&char embedding

使用两种 embedding

* word level embedding
	* 词级别emedding，使用腾讯开源词向量：https://ai.tencent.com/ailab/nlp/embedding.html
	* 基于jieba、词向量的最长匹配分词方法
* charactor level embedding
	* 字级别embedding，使用bert开源中文模型： https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip
	* 参考bert tokenization方法，增加全角、半角转换
