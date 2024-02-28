#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: YS
CreatedDate: 2023/12/13
Path:
Description: 
'''



error = '''
You are an experienced  Python teacher. Your task is to analyze an incomplete code written by a student and
then determine why the student is unable to complete the given programming task.
We have identified two common difficulties encountered by students while completing Python programming tasks for you to choose from.
We also give you the option to write in your own error type if none of the options apply.
Difficult list:
0. Students fail to grasp the basic syntax of python.
1. Students do not understand the programming to be accomplished and do not have a clear grasp of the logical implementation of the entire programming task.
2. None of the above, but I have a different description (please specify in your
reasoning).

Here is the purpose of programming task:
{}
incomplete code:
{}
Why do you think the student made this mistake? Pick an option number from the Difficulty
list and provide the reason behind your choice. Format your answer with "answer" and "reason" elements
'''

strategy ='''
You are an experienced Python teacher. 
Your task is to decide what strategies you will use to help the student by analyzing an incomplete program design written by the student and the difficulties the student encounters by not completing the program design, 
again, I will give you the task the program design is to complete. And state your intentions for choosing the specific strategy. 
We will give you a list of common strategies used by teachers and the intent from which you can choose.
We also give you the option to write in your own strategy or intention if none of the options apply. 
Strategies: 
0. Demonstrate the most basic use of syntax 
1. List the logical implementation of the upcoming section of the code written by the student   
2. Other (please specify in your reasoning) 

Intentions: 
0. Strengthen students' grasp of basic python syntax 
1. Improve students' ability to think logically about programming so that they can make their own list of logics to accomplish a particular program design 
2 Other (please specify in your reasoning) 

Here is the purpose of programming task:
{} 

incomplete code:
{} 

difficulty:
{difficulty}
How would you remediate the student’s error and why? 
Pick the option number from the list of strategies and intentions and provide the reason behind your choices. 
Format your answer as: [{"strategy": #, "intention": #, "reason": "write out your reason for picking that strategy and intention"}]
'''


template_error = '''
你是一位经验丰富的Python教师。你的任务是分析一个学生编写的不完整代码，然后分析学生为什么无法完成给定的编程任务。我们为你列出了通常学生不能完成任务的原因列表以供你选择。
如果这些选项都不适用，你也可以写出自己的原因类型。

problem：
1、学生未能掌握Python的基本语法。
2、学生不理解要完成的编程内容，对整个编程任务的逻辑实现没有清晰的把握。
3、上述都不是，但有其他类型的描述（请在你的理由中具体说明）。

编程任务的目的：
{}
不完整的代码：
{}
你认为学生为什么会犯这个错误？从problem中选择一个或者多个具体的问题，不要只是序号，并提供你选择此选项的理由。请按照json格式回答，包含problem与reason元素

'''


template_strategy ='''
你是一位经验丰富的Python教师。你的任务是通过分析学生编写的不完整程序设计以及学生在完成程序设计中遇到的困难，来决定你将使用哪些策略来帮助学生。同时，我会给你一个程序设计的任务，这个任务需要完成的目的。并说明你选择特定策略的意图，我们将为你提供教师常用的策略列表和你可以选择的意图，
如果这些选项都不适用，你也可以编写自己的策略或意图。

策略：
1、演示最基本的语法使用
2、给出学生编写的代码下一部分的逻辑
3、其他更好的方式（请在你的理由中具体说明）

意图：
1、加强学生对基本Python语法的掌握
2、提高学生对编程逻辑思考的能力，使他们能够自己列出逻辑来完成特定的程序设计
3、其他（请在你的理由中具体说明）

以下是编程任务的目的：
{}

不完整的代码：
{}

未能完成任务的原因：
{}
你将选择哪种策略帮助学生？且你的意图是什么？从策略和意图列表中分别选择一个描述清楚，并提供你选择的理由。
请以json格式回答，包含“strategy”与“purpose”元素
'''





from ..Base.BaseAgent import BaseAgent
import json

class Brain(BaseAgent):
    def __init__(self,model="gpt-3.5-turbo-1106",temperature = 0,mode = None,verbal = False):
        super().__init__(model,temperature,mode,verbal)
        self.template = template_error
        self.work = ''' '''

    def judge(self,task):
        work = input("Please input your some work:")
        self.work += work
        self.Load_Prompt(self.template,[task,self.work])
        return json.loads(self.Response())

    def strategy(self,task,code,reason):
        self.Load_Prompt(template_strategy, [task,code,reason])
        return json.loads(self.Response())




if __name__ == '__main__':
    pass
