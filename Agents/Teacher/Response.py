#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: YS
CreatedDate: 2023/12/12
Path:
Description: 
'''

template = '''
你是一位经验丰富的编程助手，你将以一种有效且引导方式来帮助学生完成程序设计。
你的帮助对象正在解决的问题是关于以下主题的：{}。
他最有可能完不成任务的原因：{}
他已经完成的代码：{}
尝试的策略：{}
请给出你的帮助提示，注意不要太过于啰嗦,同时尽量不要直接给出代码
'''

from ..Base.BaseAgent import BaseAgent

class Response(BaseAgent):
    def __init__(self,model="gpt-3.5-turbo-1106",temperature = 0,mode = None,verbal = False):
        super().__init__(model,temperature,mode,verbal)
        self.template = template

    def response(self,inforamtion):
        self.Load_Prompt(self.template,inforamtion)
        return self.Response()






if __name__ == '__main__':
    pass
