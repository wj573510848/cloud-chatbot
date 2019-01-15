#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 10:24:57 2019

@author: wj
"""
#从pymongo获取词向量
#unk与pad皆为0
#词向量维度为200

import pymongo
import pickle
import numpy as np

class word2vec_from_db:
    def __init__(self):
        self.get_collection()
        self.unk='[UNK]'
        self.pad='[PAD]'
    def get_word2vec(self,words,embedding_size=200):
        word2vec={}
        word2vec[self.unk]=np.zeros(embedding_size)
        word2vec[self.pad]=np.zeros(embedding_size)
        if len(words)<1:
            return word2vec
        def get_or_list(words):
            or_list=[]
            for w in words:
                or_list.append({'word':w})
            return or_list
        or_list=get_or_list(words)
        res=self.collection.find({'$or':or_list})
        for i in res:
            word2vec[i['word']]=pickle.loads(i['vector'])
        return word2vec
    def get_collection(self):
        host='47.100.177.102'
        port=27017
        client=pymongo.MongoClient(host=host,port=port)
        db=client.introduction
        db.authenticate('wj','aoshuowj')
        self.collection=db.word2vecByTencent
class embed_encode:
    def __init__(self,tokenizer):
        self.tokenizer=tokenizer
        self.word2vec_from_db=word2vec_from_db()
        self.unk=self.word2vec_from_db.unk
        self.pad=self.word2vec_from_db.pad
    def encode(self,sentence_list,max_length):
        sentence_split_list=[]
        all_words=set()
        for sentence in sentence_list:
            sentence_split=self.tokenizer.tokenize(sentence)
            sentence_split_list.append(sentence_split)
            for word in sentence_split:
                all_words.add(word)
        word2vec_dict=self.word2vec_from_db.get_word2vec(all_words)
        sentence_encoded=[]
        sentence_mask=[]
        for sent in sentence_split_list:
            #print(sent)
            if len(sent)>max_length:
                sent=len(sent)
            sent=[word2vec_dict.get(i,word2vec_dict[self.unk]) for i in sent]
            one_mask=[1]*len(sent)
            while len(sent)<max_length:
                sent.append(word2vec_dict[self.pad])
                one_mask.append(0)
            sentence_encoded.append(sent)
            sentence_mask.append(one_mask)
        #print(sentence_encoded)
        sentence_encoded=np.array(sentence_encoded,dtype=np.float32)#batch_size,max_length,embedding_size
        sentence_mask=np.array(sentence_mask)#batch_size,max_length
        #print(sentence_encoded.shape)
        assert sentence_encoded.shape[0]==len(sentence_list)
        assert sentence_encoded.shape[1]==max_length
        assert sentence_mask.shape[0]==len(sentence_list)
        assert sentence_mask.shape[1]==max_length
        return sentence_encoded,sentence_mask