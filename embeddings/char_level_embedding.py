#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
character level embedding based on google bert open source.
https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip
"""
import re
import os
import pickle
import numpy as np
from utils import basic_functions

class embedding_tabel:
    def __init__(self):
        self.db=basic_functions.get_mongo_db()
        self.collection=self.db.char2vecByBert
    def embedding(self,id_list):
        def get_or_list(ids):
            or_list=[]
            for id_ in ids:
                or_list.append({'id':id_})
            return or_list
        or_list=get_or_list(id_list)
        res=self.collection.find({'$or':or_list})
        id2vec={}
        for i in res:
            id2vec[i['id']]=pickle.loads(i['vector'])
        id_embed_list= [id2vec[i] for i in id_list]
        return np.array(id_embed_list,dtype=np.float32)
class embed_encode:
    def __init__(self,tokenizer):
        self.tokenizer=tokenizer
        self.embedding_table=embedding_tabel()
    def encode(self,raw_string,max_length):
        line=self.tokenizer.tokenize(raw_string)
        line=[i for i in line if not re.search("^##",i)]
        raw_sentence=self.tokenizer.basic_tokenizer.tokenize(raw_string)
        if len(line)!=len(raw_sentence):
            print("ERROR: len(raw_sentence)!=len(reg_sentence) '{}'".format(raw_string))
            return [],[],''
        token_ids=self.tokenizer.convert_tokens_to_ids(line)
        if len(token_ids)>max_length:
            token_ids=token_ids[:max_length]
            raw_sentence=raw_sentence[:max_length]
        mask=[1]*len(token_ids)
        token_ids=token_ids+[0]*(max_length-len(token_ids))
        mask=mask+[0]*(max_length-len(mask))
        assert len(token_ids)==max_length
        assert len(mask)==max_length
        token_ids=self.embedding_table.embedding(token_ids)
        return token_ids,mask,raw_sentence