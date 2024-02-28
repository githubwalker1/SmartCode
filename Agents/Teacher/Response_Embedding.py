#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: YS
CreatedDate: 2023/12/12
Path:
Description:
'''
import sys
import os
# 将 search_pdf.py 所在目录添加到 sys.path
sys.path.append('C:\\Users\\pp\\Desktop\\SmartCode\\utils')
from utils.search_pdf import search_result

template = '''
你是一位经验丰富的编程助手，你将以一种有效且引导方式并且结合《python程序设计》这个课本来帮助学生完成程序设计。
你的帮助对象正在解决的问题是关于以下主题的：{}
他最有可能完不成任务的原因：{}
他已经完成的代码：{}
尝试的策略：{}
他学习的知识在《python程序设计》这本书的位置：{}
《python程序设计》中关于该主题相近的内容：{}
请给出你的帮助提示，要告诉学生他学习的知识在书中出现的位置，以及根据书中的知识，他要注意哪些其他相关知识，如果书中有例题，可以告诉他，
注意不要太过于啰嗦,同时尽量不要直接给出代码，要提示他要怎么完成任务。
'''

template_get_query = '''
你是一位精通python的大师，请根据我给的python知识点帮我生成一个问题，我将用他们来做向量数据库查询，向量数据库的来源是一本名字为《Python程序设计》的python初学课本，
请注意：
1、要求生成的问题的内容要与所给知识点相关
2、可以对所给知识点进行适当扩充，以使得生成的问题更加具有区分度
3、可以是如下几个例子：
    (1) 元组和列表在定义上有什么区别？
    (2) python中匿名函数是如何定义的？它的作用是什么
    (3) python中如何使用列表推导式？
    (4) 文件打开模式里面readall()和readline(size=-1)的区别是什么？
我所给的知识点：
{}
'''
from ..Base import BaseAgent

class Response_Embedding(BaseAgent):
    def __init__(self,model="gpt-3.5-turbo-1106",temperature = 0,mode = None,verbal = False):
        super().__init__(model,temperature,mode,verbal)
        self.template = template
        self.template_get_query = template_get_query
    def response(self,inforamtion):
        self.Load_Prompt(self.template_get_query,inforamtion[0])
        query = self.Response()
        position_list,book_content = search_result(query)
        inforamtion.append(position_list)
        inforamtion.append(book_content)
        self.Load_Prompt(self.template,inforamtion)
        return self.Response()


if __name__ == '__main__':
    test = Response_Embedding()
    test.response("hi")