#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
character level embedding based on google bert open source.
https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip
"""
import re
import os
import pickle

class embed_encode:
    def __init__(self,tokenizer):
        self.tokenizer=tokenizer
        self.embedding_table=self.get_embed_table()
    def get_embed_table(self):
        cur_dir=os.path.dirname(os.path.abspath(__file__))
        file=os.path.join(os.path.dirname(cur_dir),'pretrained_models/vocab/char_embeddings.pkl')
        with open(file,'rb') as f:
            return pickle.load(f)
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
        token_ids=self.embedding_table[token_ids]
        return token_ids,mask,raw_sentence