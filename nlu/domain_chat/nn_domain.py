#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tensorflow as tf
import os
import pickle

class nn_oov:
    def __init__(self,encode,logger):
        """
        This model is used to determine weather one specific sentence is within our definition.
        If the sentence in our definition, we will use task chat model.
        Otherwise, we will use open chat model.
        params:
            encode: encode model,transform one sentence to ids.
        """
        self.logger=logger
        self.encode=encode
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
    def predict(self,sentence_list):
        '''
        predict input sentences in defination or not
        parameters:
            sentence_list: 1.list, contains one or more sentence,2.str, one sentence
        return:
            y_predict: list,int, 0: out of defination; 1: in defination
            probs: list,float, probability of the predictions
        '''
        if isinstance(sentence_list,str):
            sentence_list=[sentence_list]
        sentence_encoded,sentence_mask=self.encode.encode(sentence_list,self.max_length)
        feed_dict={self.input_ids:sentence_encoded,
                   self.input_mask:sentence_mask}
        y_predict,probs=self.sess.run([self.y_predict,self.probs],feed_dict)
        probs=[i[j] for i,j in zip(probs,y_predict)]
        return y_predict,probs
    def pre_process(self):
        self.logger.info("Loading oov model...")
        self.cur_dir=os.path.dirname(os.path.abspath(__file__))
        self.release_dir="/".join(self.cur_dir.split("/")[:-2])+"/pretrained_models/domain_model/oov"
        self.logger.info("Restore model from '{}'".format(self.release_dir))
        self.release_model_file=os.path.join(self.release_dir,'model.ckpt')
        self.release_var_file=os.path.join(self.release_dir,'var.pkl')
        self.release_meta_file=os.path.join(self.release_dir,'model.ckpt.meta')
        with open(self.release_var_file,'rb') as f:
            self.config=pickle.load(f)
class nn_normal_domain:
    def __init__(self,encode,logger):
        """
        This model is used to predict one specific sentence in which domain.
        If the sentence in our definition, we will use task chat model.
        Otherwise, we will use open chat model.
        params:
            
        """
        self.logger=logger
        self.pre_process()
        self.encode=encode
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
    def predict(self,sentence_list):
        '''
        predict input sentences in defination or not
        parameters:
            sentence_list: 1.list, contains one or more sentence,2.str, one sentence
        return:
            y_predict: list,domain tags
            probs: list, probability of the predictions
        '''
        if isinstance(sentence_list,str):
            sentence_list=[sentence_list]
        sentence_encoded,sentence_mask=self.encode.encode(sentence_list,self.max_length)
        feed_dict={self.input_ids:sentence_encoded,
                   self.input_mask:sentence_mask}
        y_predict,probs=self.sess.run([self.y_predict,self.probs],feed_dict)
        probs=[i[j] for i,j in zip(probs,y_predict)]
        y_predict=[self.id2tag[i] for i in y_predict]
        return y_predict,probs
    def pre_process(self):
        self.logger.info("Loading domain model...")
        self.cur_dir=os.path.dirname(os.path.abspath(__file__))
        self.release_dir="/".join(self.cur_dir.split("/")[:-2])+"/pretrained_models/domain_model/domain"
        self.logger.info("Restore from '{}'".format(self.release_dir))
        self.release_model_file=os.path.join(self.release_dir,'model.ckpt')
        self.release_var_file=os.path.join(self.release_dir,'var.pkl')
        self.release_meta_file=os.path.join(self.release_dir,'model.ckpt.meta')
        with open(self.release_var_file,'rb') as f:
            self.config=pickle.load(f)
            self.id2tag=self.config['id2tag']
class domain_model_yes_no:
    def __init__(self,tokenizer):
        self.tokenizer=tokenizer
        self.graph=tf.Graph()
        with self.graph.as_default():
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
        print(p_y)
        #11
        if p_y==11:
            return True
        else:
            return False    
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
        model_dir=os.path.join(os.path.dirname(self.basic_dir),'pretrained_models/domain_model/01')
        self.model_file=os.path.join(model_dir,'model.ckpt')
        self.meta_file=os.path.join(model_dir,'model.ckpt.meta')
        var_file=os.path.join(model_dir,'var.pkl')
        with open(var_file,'rb') as f:   
            data=pickle.load(f)
            self.vars=data
