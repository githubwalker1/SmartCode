#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: YS
CreatedDate: 2024/1/19
Path:
Description: 
'''



Recognize_Recommend_Template_Ch = '''
你是一个对python编程很了解的老师，现在有一段学生练习的代码，请你先阅读他的代码。
他之前的代码如下:{}，他当前输入的代码如下:{}。
请结合他之前的代码信息，根据他的当前输入的代码，推荐一些可能需要用到的函数或者知识。
请以json形式返回，分别是当前输入代码的那些函数，然后是推荐的函数或知识，键值为function与recommend
请注意以下几点：
1、注意如果函数当前输入代码的那些函数过于简单则不需要返回该函数
2、函数和知识点需要具体一点
3.严格按照json格式生成
4.回答使用英文
'''

from Agents.Base.BaseAgent import BaseAgent
import json

class Recognize_Recommend(BaseAgent):
    def __init__(self,model="gpt-3.5-turbo-1106",temperature = 0,mode = None,verbal = False):
        super().__init__(model,temperature,mode,verbal)
        self.template = Recognize_Recommend_Template_Ch
        self.work = ''' '''

    def start(self,*previous):
        work = input("Please input your some work:")
        self.work += work
        previous_work = ''' '''
        if(len(previous) > 1):
            previous_work += previous[0]
        self.Load_Prompt(self.template,[previous_work,self.work])
        response = self.Response()
        return json.loads(response)






if __name__ == '__main__':
    import os
    os.environ['OPENAI_API_KEY'] = 'sk-Rw6PwT9JEa6uRGzt687414F8163a44EbA274C383C5A4F9Fd'
    os.environ['OPENAI_BASE_URL'] = 'https://hb.rcouyi.com/v1'

    temp = Recognize_Recommend(mode="json",temperature=0.1)
    response = temp.start()


