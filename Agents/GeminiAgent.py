#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: YS
CreatedDate: 2023/12/14
Path:
Description: 
'''



from Agents.BaseGeminiAgent import BaseGeminiAgent

import pathlib
import textwrap
import google.generativeai as genai
import PIL.Image


import os

os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"

os.environ["GOOGLE_API_KEY"] = "AIzaSyB-w_emX3F_8xKi_bj4E-04A8gu-PxOQAU"
genai.configure(api_key='AIzaSyB-w_emX3F_8xKi_bj4E-04A8gu-PxOQAU')

'''
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)
'''


#model = genai.GenerativeModel('gemini-pro')

#response = model.generate_content("What is the meaning of life?")

template = '''
你是一名经验丰富的计算机工程师，拥有丰富的编程经验并且精通各种编程语言。下面会给你一道题目，请给出具体的思路或者完成这个任务的步骤，请不要直接给出代码。
题目如下：编写一个函数来生成斐波那契数列的前 N 个数字
'''

from Agents.BaseGeminiAgent import BaseGeminiAgent
test = BaseGeminiAgent(verbal=True)
test.Load_Prompt(template)
response = test.Response()



if __name__ == '__main__':
    pass
