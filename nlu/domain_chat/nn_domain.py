#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tensorflow as tf
import os
import pickle

class nn_oov:
    def __init__(self):
        """
        This model is used to determine weather one specific sentence is within our definition.
        If the sentence in our definition, we will use task chat model.
        Otherwise, we will use open chat model.
        """
        pass
class domain_model:
    def __init__(self,tokenizer):
        self.graph=tf.Graph()
        with self.graph.as_default():
            self.tokenizer=tokenizer
            self.basic_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.get_model_vocab()
            self.saver=tf.train.import_meta_graph(self.meta_file)


            self.x = self.graph.get_tensor_by_name(self.vars['x'])
            self.seq_length = self.graph.get_tensor_by_name(self.vars['seq_length'])
            self.prob=self.graph.get_tensor_by_name(self.vars['prob'])
            self.y=self.graph.get_tensor_by_name(self.vars['y'])
            self.config=tf.ConfigProto()
            self.config.gpu_options.allow_growth=True
            self.sess=tf.Session(graph=self.graph,config=self.config)
            self.saver.restore(self.sess,self.model_file)
    
    def predict(self,sentence):
        token_ids,seq_length=self.encode(sentence,self.vars['max_length'])
        feed_dict={self.x:[token_ids],
                   self.seq_length:[seq_length]}
        prob,y=self.sess.run([self.prob,self.y],feed_dict)
        p_y=y[0]
        p_prob=prob[0][y]
        res=[(self.id2tag[i],p) for i,p in enumerate(prob[0])]
        res=sorted(res,key=lambda x:x[1],reverse=True)
        return self.id2tag[p_y],p_prob,res
    
    def encode(self, raw_string, max_length):
        line=self.tokenizer.tokenize(raw_string)
        token_ids=self.tokenizer.convert_tokens_to_ids(line)
        if len(token_ids)>max_length:
            token_ids=token_ids[:max_length]
        seq_length=len(token_ids)
        token_ids=token_ids+[0]*(max_length-len(token_ids))
        assert len(token_ids)==max_length
        return token_ids,seq_length
        
    def get_model_vocab(self):
        model_dir=os.path.join(os.path.dirname(self.basic_dir),'pretrained/domain_model')
        self.model_file=os.path.join(model_dir,'model.ckpt')
        self.meta_file=os.path.join(model_dir,'model.ckpt.meta')
        var_file=os.path.join(model_dir,'var.pkl')
        with open(var_file,'rb') as f:   
            data=pickle.load(f)
            self.id2tag=data['id2tag']
            data.pop('id2tag')
            self.vars=data
