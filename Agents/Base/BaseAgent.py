#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: YS
CreatedDate: 2023/12/12
Path:
Description: 
'''



from openai import embeddings
import json
from openai import OpenAI

class BaseAgent():
    def __init__(self,model="gpt-3.5-turbo-1106",temperature = 0,mode = None,verbal = False):
        self.model = OpenAI()
        self.model_type = model
        self.temperature = temperature
        self.format = {"type": "json_object"} if mode == "json" else None
        self.__total_token = 0
        self.__present_token = 0
        self.__history = []
        self.__prompt = []
        self.__static = []
        self.__verbal = verbal
        self.__init()

    def Response(self,*chat,role = "user"):
        message = []
        if(len(self.__static) > 0):
            message += self.__static
        if(len(self.__prompt) > 0):
            message += self.__prompt
        if(len(self.__history) > 0):
            message += self.__history
        if(len(chat) > 0):
            message += [self.ChangeForm(chat[0],role)]

        response = self.model.chat.completions.create(
            model=self.model_type,
            temperature=self.temperature,
            response_format=self.format,
            messages=message
            )
        self.__total_token += response.usage.total_tokens
        self.__present_token = response.usage.total_tokens
        if self.__verbal:
            print(response.choices[0].message.content)
        return response.choices[0].message.content
        #return response.choices[0]

    def run(self,*var,role = "user"):
        if(len(var) > 0):
            chat = var[0]
        else:
            chat = input("Please input:")
        self.__history.append(self.ChangeForm(chat,role))
        response = self.Response(chat)
        self.__history.append(self.ChangeForm(response,"assistant"))
        return response


    def Load_Prompt(self,prompt,*var,role = "user"):
        temp = prompt
        prompt_type = type(prompt)
        if (prompt_type == dict):
            if (len(var) > 0):
                if (type(var[0]) == list):
                    if (len(var[0]) == 1):
                        temp["content"] = prompt["content"].format(var[0][0])
                    else:
                        temp["content"] = prompt["content"].format(*var[0])
                if (type(var[0]) == dict):
                    temp["content"] = prompt["content"].format(**var[0])
                if (type(var[0]) == str):
                    temp["content"] = prompt["content"].format(var[0])
            self.__prompt = [temp]
        if (prompt_type == str):
            if (len(var) > 0):
                if (type(var[0]) == list):
                    if (len(var[0]) == 1):
                        temp = prompt.format(var[0][0])
                    else:
                        temp = prompt.format(*var[0])
                if (type(var[0]) == dict):
                    temp = prompt.format(**var[0])
                if (type(var[0]) == str):
                    temp = prompt.format(var[0])
            self.__prompt = [self.ChangeForm(temp,role)]
        #print(temp)

    def Full_Prompt(self,prompt,*var):
        temp = prompt
        prompt_type = type(prompt)
        if (prompt_type == dict):
            if (len(var) > 0):
                temp["content"] = prompt["content"].format(*var[0])
            return temp
        if (prompt_type == str):
            if (len(var) > 0):
                temp = temp.format(*var[0])
            return temp

    def __init(self):
        if self.format != None:
            self.__static.append({"role": "system", "content": "You are a helpful assistant designed to strictly output JSON."})



    def ChangeForm(self,info,role = "user"):
        return {"role":role,"content":info}

    def Emembedding(self,input,model = "text-embedding-ada-002"):
        response = self.model.embeddings.create(
            input=input,
            model=model
        )
        self.__total_token += response.usage.total_tokens
        return response.data[0].embedding
        #return response

    def __CheckError(self,input):
        pass

    def AddMessage(self,info,role = "user"):
        self.__history.append({"role":role,"content":info})


    def Save_Hisrtoy(self):
        pass

    def Clear(self):
        self.__history.clear()


    def ResetPara(self,model="gpt-3.5-turbo-1106",temperature = 0,mode = None):
        pass

    def AddHistory(self,history):
        self.__history += history

    def ExportHistory(self):
        return self.__history

    def ExportMessage(self,message,role = "user"):
        return self.ChangeForm(message,role)

    def Total_Token(self):
        return self.__total_token

    def Present_Token(self):
        return self.__present_token


    def AllPrompt(self):
        print(self.__static)
        print(self.__prompt)
        print(self.__history)

    def Info(self):
        print("Total tokens:",self.__total_token)
        print("Present tokens:" , self.__present_token)






if __name__ == '__main__':
    import os
    os.environ["OPENAI_API_KEY"] = ""

    temp = {"role": "user", "content": "HI"}
    #temp =  {"role": "user","content": "请帮我写个代码，要求给出斐波那契数列的第八个质数 "}
    test = BaseAgent(verbal=True)
    #test.Load_Prompt("hi{}",["ss","sssssssss"])
    a = test.Response("HI")
    test.AddMessage(a,"assistant")
    test.Info()
    #test.AllPrompt()
