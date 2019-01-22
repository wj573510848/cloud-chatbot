#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 22 16:02:58 2019

@author: wj
"""

from nlu.domain_chat import nn_domain,nn_intent,nn_slot,template_dis

class in_domain_model:
    def __init__(self,word_level_encoder,char_level_encoder,logger):
        self.logger=logger
        self.dis_model=template_dis.template_task_model(self.logger)
        self.nn_domain_model=nn_domain.nn_normal_domain(word_level_encoder,logger)
        self.nn_oov_model=nn_domain.nn_oov(word_level_encoder,logger)
        self.nn_intent_model={
                'weather':nn_intent.nn_normal_intent(word_level_encoder,'weather',logger),
                'phone':nn_intent.nn_normal_intent(word_level_encoder,'phone',logger)
                }
        self.nn_slot_model={
                'weather':nn_slot.nn_normal_slot(char_level_encoder,'weather',logger),
                'phone':nn_slot.nn_normal_slot(char_level_encoder,'phone',logger)
                    }
        self.domain_intent={'weather':['query'],
                            'phone':'call'}
    def domain_predict(self,sentence,domain,intent):
        self.logger.info("specific domain predict for sentence:{}".format(sentence))
        res=self.dis_model.predict(sentence)
        if res:
            self.logger.info("get results by dis model")
            self.logger.info("results:{}".format(res))
            return res
        if intent not in self.domain_intent[domain]:
            self.logger.info('the specific intent {} not in domain'.format(intent))
            return self.normal_predict(sentence)
        domain_pre,status=self.get_domain_specific(sentence)
        if status:
            if domain_pre ==domain or domain_pre=='null':
                return self.normal_outputs(domain,intent,self.get_slot_normal(sentence,domain))
            else :
                return self.normal_predict(sentence)
        return self.null_results()
    def normal_predict(self,sentence):
        self.logger.info("normal domain predict for sentence:{}".format(sentence))
        res=self.dis_model.predict(sentence)
        if res:
            self.logger.info("get results by dis model")
            self.logger.info("results:{}".format(res))
            return res
        domain=self.get_domain_normal(sentence)
        if domain=='null':
            return self.null_results()
        intent=self.get_intent_normal(sentence,domain)
        if intent=='null':
            return self.null_results()
        slots=self.get_slot_normal(sentence,domain)
        return self.normal_outputs(domain,intent,slots)
    def normal_outputs(self,domain,intent,slots):
        return {'domain':domain,'intent':intent,'slots':slots}
    def null_results(self):
        return {'domain':'null','intent':'null','slots':[]}
    def get_slot_normal(self,sentence,domain):
        if domain not in self.nn_slot_model:
            return []
        slots=self.nn_slot_model[domain].predict(sentence)
        self.logger.info("slot predict:{}".format(slots))
        return slots
    def get_intent_normal(self,sentence,domain):
        if domain not in self.nn_intent_model:
            return 'null'
        nn_intent_res,score=self.nn_intent_model[domain].predict(sentence)
        self.logger.info("intent predict:{},{}".format(nn_intent_res,score))
        if nn_intent_res not in self.domain_intent[domain]:
            return 'null'
        return nn_intent_res
    def get_domain_normal(self,sentence,oov_score=0.75):
        oov_y,oov_prob=self.nn_oov_model.predict(sentence)
        oov_y=oov_y[0]
        oov_prob=oov_prob[0]
        self.logger.info("oov predict:{}, {}".format(oov_y,oov_prob))
        if oov_y==0 and oov_prob>oov_score:
            return 'null'
        else:
            domain_p,domain_score=self.nn_domain_model.predict(sentence)
            domain_p=domain_p[0]
            domain_score=domain_score[0]
            self.logger.info("domain predict:{}, {}".format(domain_p,domain_score))
            if domain_p not in ['weather','phone']:
                return 'null'
            else:
                return domain_p
    def get_domain_specific(self,sentence,oov_score=0.75):
        '''
        返回三种情况：
        1.domain=weather or phone status=True
        2.domain not in [weather,query] not in oov domain='null',status=False
        3.domain in oov domain='null' status=True
        '''
        oov_y,oov_prob=self.nn_oov_model.predict(sentence)
        oov_y=oov_y[0]
        oov_prob=oov_prob[0]
        self.logger.info("oov predict:{}, {}".format(oov_y,oov_prob))
        if oov_y==0 and oov_prob>oov_score:
            return 'null',True
        else:
            domain_p,domain_score=self.nn_domain_model.predict(sentence)
            domain_p=domain_p[0]
            domain_score=domain_score[0]
            self.logger.info("domain predict:{}, {}".format(domain_p,domain_score))
            if domain_p not in ['weather','phone','null']:
                return 'null',False
            else:
                return domain_p,True
            
        
        