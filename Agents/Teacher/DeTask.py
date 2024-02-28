#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: YS
CreatedDate: 2023/12/13
Path:
Description: 
'''

from ..Base.BaseAgent import BaseAgent



template = '''
你是一名经验丰富的计算机工程师，拥有丰富的编程经验并且精通各种编程语言。下面会给你一道题目，请给出具体的思路或者完成这个任务的步骤，请不要直接给出代码。
题目如下：{}
'''


class DeTask(BaseAgent):
    def __init__(self,model="gpt-3.5-turbo-1106",temperature = 0,mode = None,verbal = False):
        super().__init__(model,temperature,mode,verbal)
        self.template = template

    def detask(self):
        problem = input("Please print your problem:")
        self.Load_Prompt(self.template,problem)
        return self.Response()




if __name__ == '__main__':
    temp = {"role": "user","content": "Hi {}"}
    # temp =  {"role": "user","content": "请帮我写个代码，要求给出斐波那契数列的第八个质数 "}
    test = DeTask(verbal=True)

    #test.Load_Prompt(temp)
    #test.run("Hi")
    #a = test.Response("HI")
    #test.AddMessage(a, "assistant")

    res = test.detask()







    test.Info()


