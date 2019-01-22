#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: wj
基于模板的意图提取模型
#需要两类文件
#1.basic_template.txt 基础模板
#2.模板涉及到的slot列表，命名规则phone_number.slotlist
#3.取消，确认，退出，选择使用该模板实现
#4.control:no,yes,exit,select,selectReverse
"""
import os
import re
import collections
import glob
from utils import basic_functions

class template_task_model:
    def __init__(self,logger):
        self.logger=logger
        self._pre_process()
    def predict(self,sentence):
        try:
            sentence=basic_functions.to_arabic_numerals(sentence)
            res=self.match_basic_template(sentence)
            return res
        except:
            self.logger.error("Something wrong with dis model. Sentence:{}".format(sentence))
            return ''
    def match_basic_template(self,sentence):
        for key in self.basic_template:
            re_res=re.search(key,sentence)
            if re_res:
                groupdict=re_res.groupdict()
                domain_intent=self.basic_template[key]
                status=True
                for g_key in groupdict:
                    qurey_key=domain_intent.split('_')[0]+'_'+g_key
                    slot_value=self.reg_words(groupdict[g_key])
                    if self.basic_slot_validate(qurey_key,slot_value) is False:
                        status=False
                        break
                if status:
                    self.logger.info("matched template:{},{}".format(self.basic_template[key],key))
                    return self.conver_basic_template_to_normal_style(domain_intent.split('_')[0],domain_intent.split('_')[1],groupdict)
        return ''
    def conver_basic_template_to_normal_style(self,domain,intent,slot_dict):
        res={}
        res['domain']=domain
        res['intent']=intent
        res['slots']=[]
        for key in slot_dict:
            res['slots'].append({'name':key,'rawValue':slot_dict[key],'regValue':slot_dict[key]})
        return res
    def basic_slot_validate(self,scope,slot_value):
        if slot_value in self.validate_slot_dict[scope]:
            return True
        return False
    
    def reg_words(self,words):
        words=words.lower()
        words=re.sub('\s','',words)
        return words
    def _pre_process(self):
        basic_template_file=os.path.join(basic_functions.get_root_dir(),'pretrained_models/qa/template/basic_template.txt')
        slot_files=glob.glob(os.path.join(basic_functions.get_root_dir(),'pretrained_models/qa/template/*.slotlist'))
        self.logger.info("Load basic template file:{}".format(basic_template_file))
        self.logger.info("Load slot files:{}".format(basic_template_file))
        #regular template
        self.basic_template={}
        for line in basic_functions.read_lines(basic_template_file):
            if line[0]=='#':
                continue
            domain_intent,expression =self.convert_basic_template_line(line)
            if expression:
                self.basic_template[expression]=domain_intent
        self.validate_slot_dict=collections.defaultdict(set)
        for file in slot_files:
            domain_slot=file.split('/')[-1][:-9]
            for line in basic_functions.read_lines(file):
                line=self.reg_words(line)
                self.validate_slot_dict[domain_slot].add(line)
    def convert_basic_template_line(self,line):
        line=line.split()
        if len(line)<2:
            return '',''
        domain_intent=line[0]
        line="".join(line[1:])
        re_line=[]
        for i in re.split("(<[a-zA-Z]+/>)",line):
            if i:
                if re.search("<[a-zA-Z]+/>",i):
                    re_line.append('(?P<{}>.+)'.format(i[1:-2]))
                    continue
                else:
                    re_line.append(self.reg_words(i))
        if len(re_line)<1:
            return '',''
        re_line="{}{}{}".format("^","".join(re_line),"$")
        return domain_intent,re_line