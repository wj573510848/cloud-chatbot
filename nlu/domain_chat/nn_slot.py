#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wj
"""
import tensorflow as tf
import os
import re
import pickle
class nn_normal_slot:
    def __init__(self,encode,domain,logger):
        self.logger=logger
        self.encode=encode
        self.domain=domain
        self.pre_process()
        self.graph=tf.Graph()
        with self.graph.as_default():
            self.saver=tf.train.import_meta_graph(self.release_meta_file)
            self.input_ids=self.graph.get_tensor_by_name(self.config['x'])
            self.input_mask=self.graph.get_tensor_by_name(self.config['mask'])
            self.max_length=self.config['max_length']
            self.tags=self.graph.get_tensor_by_name(self.config['tags'])
            self.config=tf.ConfigProto()
            self.config.gpu_options.allow_growth=True
            self.sess=tf.Session(graph=self.graph,config=self.config)
            self.saver.restore(self.sess,self.release_model_file)
    def predict(self,sentence,debug=None):
        token_ids,mask,reg_sentence=self.encode.encode(sentence,self.max_length)
        if len(token_ids)<1:
            return []
        feed_dict={self.input_ids:[token_ids],
                   self.input_mask:[mask]}
        tags=self.sess.run(self.tags,feed_dict)
        crf_tags=tags[0]
        crf_tags=[self.id2tag[i] for i in crf_tags]
        crf_tags=crf_tags[:len(reg_sentence)]
        return self._to_normal_style(reg_sentence,crf_tags)
    def _to_normal_style(self,sentence,tags):
        assert len(sentence)==len(tags)
        slots=[]
        B_tag_ids=[i for i,j in enumerate(tags) if j[0]=="B"]
        if len(B_tag_ids)==0:
            return slots
        for index in B_tag_ids:
            sub=self._basic_slot_style()
            slot_name=tags[index][2:]
            raw_values=sentence[index]
            for w,t in zip(sentence[index+1:],tags[index+1:]):
                if t=="M_"+slot_name:
                    if re.search('[a-zA-Z]$',raw_values):
                        raw_values=raw_values+" "+w
                    elif re.search('^[a-zA-Z]',w):
                        raw_values=raw_values+" "+w
                    else:
                        raw_values=raw_values+w
                else:
                    break
            sub['name']=slot_name
            sub['rawValue']=raw_values
            sub['regValue']=raw_values
            slots.append(sub)
        return slots
    def _basic_slot_style(self):
        dic = {}
        dic['name']=''
        #dic['score']=[]
        dic['rawValue']=''
        dic['regValue']=''
        return dic 
    def pre_process(self):
        self.cur_dir=os.path.dirname(os.path.abspath(__file__))
        self.logger.info("Loading slot model for '{}'...".format(self.domain))
        self.release_dir="/".join(self.cur_dir.split("/")[:-2])+"/pretrained_models/domain_model/slot/{}".format(self.domain)
        self.logger.info("Restore from '{}'".format(self.release_dir))
        self.release_model_file=os.path.join(self.release_dir,'model.ckpt')
        self.release_var_file=os.path.join(self.release_dir,'var.pkl')
        self.release_meta_file=os.path.join(self.release_dir,'model.ckpt.meta')
        
        with open(self.release_var_file,'rb') as f:
            self.config=pickle.load(f)
            self.id2tag=self.config['id2tag']