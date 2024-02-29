#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: YS
CreatedDate: 2023/12/13
Path:
Description: 
'''

import os
os.environ["OPENAI_API_KEY"] = ""
#os.environ["OPENAI_API_KEY"] = ""


from Agents.Teacher.DeTask import DeTask
from Agents.Teacher.Brain import Brain
from Agents.Teacher.Response import Response
from Agents.Teacher.Response_Embedding import Response_Embedding
import json

total = 0

Task = DeTask(verbal=True,model="gpt-3.5-1106-preview")
Brain = Brain(verbal=True,mode="json",model="gpt-3.5-1106-preview")
#Response = Response(verbal=True,model="gpt-4-1106-preview")
Response = Response_Embedding(verbal=True,model="gpt-3.5-1106-preview")


detask = Task.detask()
while(1):
    problem = Brain.judge(detask)
    strategy = Brain.strategy(detask,Brain.work,problem["reason"])
    Response.response([detask,problem["reason"],Brain.work,strategy["strategy"]])




#print("Total Token:",DeTask.Total_Token()+Brain.Total_Token()+Response.Total_Token())




if __name__ == '__main__':
    pass
