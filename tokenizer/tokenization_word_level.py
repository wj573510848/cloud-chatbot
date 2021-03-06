#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
word level tokenizer based on jieba and tencent open source.
https://pypi.org/project/jieba/
https://ai.tencent.com/ailab/nlp/embedding.html
"""
import re
import jieba

import sys
sys.path.append("../")
from utils import basic_functions


class vocab_from_db:
    def __init__(self):
        self.db=basic_functions.get_mongo_db()
        self.collection=self.db['wordLevelVocab']
def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换            
            inside_code = 32 
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248
        rstring += chr(inside_code)
    return rstring

class jieba_based_tokenizer:
    def __init__(self,lower=True,logger=None):
        if logger is not None:
            logger.info("initialize word level tokenizer...")
        self.unk='[UNK]'
        self.pad='[PAD]'
        self.vocab=vocab_from_db()
        self.lower=lower
        self.unk_id=self.vocab.collection.find_one({'word':self.unk})['id']
        self.pad_id=self.vocab.collection.find_one({'word':self.pad})['id']
        if logger is not None:
            logger.info("vocab size:{}".format(self.vocab.collection.count()))
    def tokenize(self,sentence):
        word_list=self.basic_split(sentence)
        return self.full_cut(word_list)
    def full_cut(self,word_list):
        words=[]
        for word in word_list:
            if self.vocab.collection.find_one({'word':word}):
                words.append(word)
            else:
                words.extend(self.cut_by_vocab(word))
        return words
    def cut_by_vocab(self,word):
        #str_word=[i for i in word]
        #str_word.reverse()
        #word="".join(str_word)
        #new_list=[]
        #end=len(word)
        #while end>0:
        #    status=False
        #    for start in range(end):
        #        if word[start:end] in self.vocab:
        #            new_list.append(word[start:end])
        #            end=start
        #            status=True
        #            break
        #    if not status:
        #        new_list=[self.unk]
        #        break
        #new_list.reverse()
        #return new_list
        start=0
        new_list=[]
        while start<len(word):
            end=len(word)
            status=False
            while end>start:
                if self.vocab.collection.find_one({'word':word[start:end]}):
                #if word[start:end] in self.vocab:
                    new_list.append(word[start:end])
                    start=end
                    status=True
                    break
                end=end-1
            if not status:
                new_list=[self.unk]
                break
        return new_list
            
    def basic_split(self,sentence):
        '''
        汉字，数字，英文使用正则切分
        汉字及符号，使用jieba切分
        '''
        sentence=strQ2B(sentence)
        if self.lower:
            sentence=sentence.lower()
        sentence=re.sub(r"[ ]+([\u4e00-\u9fa5]+)[ ]*",r"\1",sentence)
        sentence=re.sub(r"[ ]*([\u4e00-\u9fa5]+)[ ]+",r"\1",sentence)
        sentence=re.split("([\u4e00-\u9fa5]+|[a-zA-Z]+|[0-9]+)",sentence)
        sentence=[i.strip() for i in sentence]
        sentence=[i for i in sentence if i]
        res=[]
        for s in sentence:
            if re.search('[a-zA-Z0-9]',s):
                res.append(s)
            else:
                res.extend(jieba.lcut(s))
        res_splited = [i for i in res if i]
        return " ".join(res_splited).split()
    def convert_tokens_to_ids(self,tokens):
        new_list=[]
        for token in tokens:    
            res= self.vocab.collection.find_one({'word':token})
            if not res:
            #if token not in self.vocab:
                print("{} not in vocab?".format(token))
                new_list.append(self.unk_id)
            else:
                new_list.append(res['id'])
        return new_list
