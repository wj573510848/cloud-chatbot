#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wj
"""

import tensorflow as tf
import os
import pickle

class nn_normal_intent:
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
            self.logits=self.graph.get_tensor_by_name(self.config['logits'])
            self.y_predict=tf.argmax(self.logits,axis=-1)
            self.probs=tf.nn.softmax(self.logits,-1)
            self.config=tf.ConfigProto()
            self.config.gpu_options.allow_growth=True
            self.sess=tf.Session(graph=self.graph,config=self.config)
            self.saver.restore(self.sess,self.release_model_file)
    
    def predict(self,sentence,debug=None):
        sentence_encoded,sentence_mask=self.encode.encode([sentence],self.max_length)
        feed_dict={self.input_ids:sentence_encoded,
                   self.input_mask:sentence_mask}
        y_predict,probs=self.sess.run([self.y_predict,self.probs],feed_dict)
        probs=[i[j] for i,j in zip(probs,y_predict)]
        y_predict=[self.id2tag[i] for i in y_predict]
        return y_predict[0],probs[0]
    
    def pre_process(self):
        self.cur_dir=os.path.dirname(os.path.abspath(__file__))
        self.logger.info("Loading intent model for '{}'...".format(self.domain))
        self.release_dir="/".join(self.cur_dir.split("/")[:-2])+"/pretrained_models/domain_model/intent/{}".format(self.domain)
        self.logger.info("Restore from '{}'".format(self.release_dir))
        self.release_model_file=os.path.join(self.release_dir,'model.ckpt')
        self.release_var_file=os.path.join(self.release_dir,'var.pkl')
        self.release_meta_file=os.path.join(self.release_dir,'model.ckpt.meta')
        with open(self.release_var_file,'rb') as f:
            self.config=pickle.load(f)
            self.id2tag=self.config['id2tag']