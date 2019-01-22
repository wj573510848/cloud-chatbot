#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 10:18:04 2019

@author: wj
"""
import pickle
import numpy as np
import os
import copy
import time
import random
import re
from utils import basic_functions
from utils import bot_config
class sentence_encode_by_word2vec:
    '''
    encode one sentence to a vector.
    '''
    def __init__(self,tokenizer):
        self.tokenizer=tokenizer
        self.db=basic_functions.get_mongo_db()
        self.collection=self.db.word2vecByTencent
        self.unk_array=np.zeros(200)
    def sentence_encode(self,sentence):
        sentence=self.tokenizer.tokenize(sentence)
        words=set(sentence)
        word2vec={}
        def get_or_list(words):
            or_list=[]
            for w in words:
                or_list.append({'word':w})
            return or_list
        or_list=get_or_list(words)
        res=self.collection.find({'$or':or_list})
        for i in res:
            word2vec[i['word']]=pickle.loads(i['vector'])
        vectors=[word2vec.get(i,self.unk_array) for i in sentence]
        vector=np.average(vectors,axis=0)
        return vector
class chat_model:
    def __init__(self,tokenizer):
        self._pre_load()
        self.sentence_vec_model=sentence_encode_by_word2vec(tokenizer)
    def response(self,sentence,score=0.95,default_answer=None):
        if default_answer is None:
            default_answer=None
        matched_question,matched_answer,q_rate=self.get_top_one_response(sentence)
        if q_rate>score:
            answer=self.regular_answer(matched_answer)
            if answer is None:
                return default_answer
            else:
                return answer
        else:
            return default_answer
    def regular_answer(self,answer):
        '''
        将answer中的bot信息替换
        '''
        answer=re.split("(<[a-zA-Z]+>)",answer)
        res=[]
        for a in answer:
            if re.search("<[a-zA-Z]+>",a):
                a=a[1:-1]
                a=self.bot_info.get(a,'')
                if not a:
                    return None
                res.append(a)
            else:
                res.append(a)
        return "".join(res)
    def get_top_one_response(self,sentence):
        similar_q_ids=self.get_similar_question_ids(sentence)
        q_ids=[]
        q_rate=0
        for id_,rate in similar_q_ids:
            if len(q_ids)==0:
                q_ids.append(id_)
                q_rate=rate
            else:
                if rate==q_rate:
                    q_ids.append(id_)
                else:
                    break
        q_id=int(random.choice(q_ids))
        matched_question=self.get_question(q_id)
        matched_answer=self.match_answer(q_id)
        return matched_question,matched_answer,q_rate
    def match_answer(self,q_id):
        a_ids=self.relation_collection.find_one({'qid':q_id})['aids']
        a_ids=pickle.loads(a_ids)
        if len(a_ids)<1:
            return None
        a_id=random.choice(list(a_ids))
        answer=self.answer_collection.find_one({'aid':a_id})['answer']
        return answer
    def get_similar_question_ids(self,sentence,top_n=5):
        sentence_vector=self.sentence_vec_model.sentence_encode(sentence)
        center_id=self.get_cluster(sentence_vector)
        similar_q_ids=self.compute_question_similar(sentence_vector,center_id,top_n)
        return similar_q_ids
    def compute_question_similar(self,vector,center_id,top_n=5):
        vector_file=os.path.join(self.question_candidate_dir,'question_vector_{}.pkl'.format(center_id))
        with open(vector_file,'rb') as f:
            vectors,vectors_norms,q_ids=pickle.load(f)
        rank_index,rank=self.compute_cosin_distance(vector,vectors,None,vectors_norms)
        similar_q_ids=[]
        for i in range(top_n):
            similar_q_ids.append((q_ids[rank_index[i]],rank[rank_index[i]]))
        return similar_q_ids
    def compute_cosin_distance(self,vec1,vec2,vec1_norm=None,vec2_norm=None):
        if not isinstance(vec1,np.ndarray):
            vec1=np.array(vec1)
        if not isinstance(vec2,np.ndarray):
            vec2=np.array(vec2)
        if vec1_norm is None:
            vec1_norm=np.linalg.norm(vec1)
        if vec2_norm is None:
            vec2_norm=np.linalg.norm(vec2,axis=-1)
        multi_norm=vec1_norm*vec2_norm
        multi_norm=[i if i!=0 else 1 for i in multi_norm]
        rank=np.dot(vec2,vec1)/multi_norm
        rank_index=np.argsort(rank)[::-1]
        return rank_index,rank
    def _pre_load(self):
        db=basic_functions.get_mongo_db()
        root_dir=basic_functions.get_root_dir()
        #kmeans clster
        kmeans_cluster_file=os.path.join(root_dir,'pretrained_models/qa/centers.pkl')
        with open(kmeans_cluster_file,'rb') as f:
            self.kmeans_centers=pickle.load(f)
        self.qustion_collection=db.matchQaQuestions
        self.answer_collection=db.matchQaAnswers
        self.relation_collection=db.matchQaRelation
        self.question_candidate_dir=os.path.join(root_dir,'pretrained_models/qa')
        self.bot_info=bot_config.bot_profile().bot_basic_info
    def get_cluster(self,x):
        x_np=np.array(copy.deepcopy(x))
        def euclidean(x,y):
            x=np.array(x)
            y=np.array(y)
            x_y=x-y
            return np.linalg.norm(x_y)
        euclidean_distances=[euclidean(x_np,i) for i in self.kmeans_centers]
        return np.argmin(euclidean_distances,axis=-1)
    def get_question(self,id_):
        return self.qustion_collection.find_one({'qid':id_})['question']
        
    