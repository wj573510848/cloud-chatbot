#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 20 15:17:58 2019

@author: wj
"""

#https://dash.plot.ly/
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html

from utils import basic_log,basic_config
from tokenizer import tokenization_word_level
from nlu.open_chat.match_based_qa import chat_model

config=basic_config.config()
logger=basic_log.get_logger('chatbot',config.log_file)
word_tokenizer=tokenization_word_level.jieba_based_tokenizer(logger=logger)
chat=chat_model(word_tokenizer)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
markdown_text='''
#### 这是chabot测试

* 在文本框中输入信息

- 点击提交

'''
def get_cur_time():
    t_now=datetime.datetime.now()
    h=t_now.hour
    m=t_now.minute
    s=t_now.second
    return "{}:{}:{}".format(h,m,s)
raw_string=[]
error_too_long='输入太长，输入长度需小于64'
app.layout = html.Div([
        html.H1(children='您好，我是机器人小诗'),
        dcc.Markdown(children=markdown_text),
        dcc.Textarea(id='output',style={'width': '100%','min-height': '200px'},readOnly=True,rows=8,wrap=False,autoFocus=True),
        dcc.Input(id='input', value='', type='text',style={'width': '30%'},maxlength='64',placeholder='最多输入64个字符',debounce=True),
        html.Button('提交', id='button'),

],style={'columnCount': 1})
@app.callback(
    dash.dependencies.Output('output', 'value'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input', 'value')],)
def update_output(submit_click,input_value):
    global raw_string
    if submit_click:
        if len(input_value)>64 or len(input_value)<1:
            q="user({}): ".format(get_cur_time())+input_value[:10]+'......'
            a='chat({}): '.format(get_cur_time())+error_too_long
        else:
            q="user({}): ".format(get_cur_time())+input_value
            chat_answer=chat.response(input_value)
            chat_answer=chat_answer[:64]
            a='chat({}): '.format(get_cur_time())+chat_answer
        raw_string.append(q)
        raw_string.append(a)
        raw_string=raw_string[-8:]
        return "\n".join(raw_string)
    else:
        return ''
#gunicorn -b 192.168.1.8:8000 app4:server
#if __name__ == '__main__':
#    app.run_server(debug=False,host='192.168.1.8')