import networkx as nx
import json
import os
from tqdm import tqdm
from collections import deque


def id_to_concept(data:list,file:str = './/Data//KG//id_function.json'):
    if(len(data) > 0):
        with open(file, 'r') as trans_name:
            name = json.load(trans_name)
        if isinstance(data[0],list):
            for i in range(len(data)):
                for j in range(len(data[i])):
                    data[i][j] = name[data[i][j]]
        else:
            for i in range(len(data)):
                data[i] = name[data[i]]
def concept_to_id(data:list,file:str = './/Data//KG//function_id.json'):
    if(len(data) > 0):
        with open(file, 'r') as trans_name:
            name = json.load(trans_name)
        if isinstance(data[0],list):
            for i in range(len(data)):
                for j in range(len(data[i])):
                    data[i][j] = name[data[i][j]]
        else:
            for i in range(len(data)):
                    data[i] = name[data[i]]

def find_graph_path(start:list,end:list,k:int = 4,min_num:int = 3,max_cur = 10,data_file:str = '..//Data//KG//transformed_data.json') -> list:
    if len(start) <= 0 or len(end) <= 0 or k <= 0:
        return []
    else:
        result = []
        with open(data_file, 'r') as file:
            kg = json.load(file)
            for begin in start:
                for endpoint in end:
                    if (begin in kg) and (endpoint in kg):
                        result += bfs_find_path(kg,begin,endpoint,k)
            if len(result) < min_num and max_cur > 0:
                result = find_graph_path(start,end,k+1,min_num,max_cur-1,data_file)
        return result

def bfs_find_path(data,start,end,k: int) ->list:     #广度深度搜索
    if (len(data[start].keys()) == 0):
        return []
    else:
        temp = 1
        queue = deque([(start, [start])])
        final_path = []
        level_count = [] #各层级数量列表
        level_count.append(len(data[start].keys()))
        level_count.append(0)
        while queue and len(level_count) <= k+1:   #确保深度
            current, path = queue.popleft()
            for node in data[current].keys():
                # 确定层数
                if(len(level_count) < k+1):
                    level_count[-1] += len(data[node].keys())  #下层数相加
                    #if current in data[node].keys():   #避免双向图重复添加
                     #   level_count[-1] -= 1

                #节点操作
                if node not in path:  #防止回环
                    new_path = path + [node]
                    if node == end:
                        final_path.append(new_path)
                    else:
                        queue.append((node, new_path))
                level_count[-2] -= 1   #上层减1
            # 判断是否上层遍历完毕，完毕则下一层的下一层开始计数
            if (level_count[-2] <= 0):
                level_count.append(0)
            #print(temp,level_count[-2],level_count[-1])
            temp += 1
        return final_path

def find_node_k_hop(start:list,k:int=2,data_file:str = './/Data//KG//transformed_data.json') ->list:    #查找k跳的图中节点
    if len(start) <= 0:
        return []
    else:
        result = []
        with open(data_file, 'r') as file:
            kg = json.load(file)
        dfs_find_node(kg,start,result,k)
        result_unique = list(set(result)) #处理重复节点
        return result_unique

def dfs_find_node(data,start:list,result:list,k: int):     #递归深度搜索
    if k > 0 and len(start) > 0:
        for item in start:     #开始节点
            if item in data:  # 确定是否在kg中
                neighbours = list(data[item].keys())    #临接节点
            else:
                continue
            if len(neighbours) > 0:
                for item_neighbour in data[item].keys():  # 对应id的关系对
                    result.append(item_neighbour)
                dfs_find_node(data,neighbours, result, k - 1)
    else:
        return




def load_resources(cpnet_vocab_path):
    global concept2id, id2concept, relation2id, id2relation

    with open(cpnet_vocab_path, "r", encoding="utf8") as fin:
        id2concept = [w.strip() for w in fin]
    concept2id = {w: i for i, w in enumerate(id2concept)}

    #id2relation = merged_relations
    relation2id = {r: i for i, r in enumerate(id2relation)}


def load_cpnet(cpnet_graph_path):
    global cpnet, cpnet_simple
    cpnet = nx.read_gpickle(cpnet_graph_path)
    cpnet_simple = nx.Graph()
    for u, v, data in cpnet.edges(data=True):
        w = data['weight'] if 'weight' in data else 1.0
        if cpnet_simple.has_edge(u, v):
            cpnet_simple[u][v]['weight'] += w
        else:
            cpnet_simple.add_edge(u, v, weight=w)

def get_unique_concept(data) -> list:
    if (len(data) > 0):
        result = []
        if isinstance(data[0], list):
            for i in range(len(data)):
                for j in range(len(data[i])):
                    if data[i][j] not in result:
                        result.append(data[i][j])
        else:
            for i in range(len(data)):
                if data[i] not in result:
                    result.append(data[i])
        return result
    else:
        return []





if __name__ == '__main__':
    graph = {
        'A': {'B':[0,1], 'C':[0,1]},
        'B': {'D':[2], 'E':[2,3]},
        'C': {'F':[3]},
        'D': {},
        'E': {'F':[2]},
        'F': {'A':[1]},
    }

    test_start = ['A','B']
    result = []
    temp = dfs_find_node(graph,test_start,result,2)
    #a = bfs_find_path(graph,"A","F",3)
    #b = find_graph_path(graph,["A","B"],["F","D"],2)   #不可用

    graph_double = {
        'A': {'B': [0, 1], 'C': [0, 1],"F":[1]},
        'B': {'D': [2], 'E': [2, 3],"A":[0,1]},
        'C': {'F': [3],"A":[0,1]},
        'D': {"B":[2]},
        'E': {'F': [2],"B":[2,3]},
        'F': {'A': [1],"C":[3]},
    }
    bfs_find_path(graph_double, "B", "D", 10)
    result_temp = []
    for begin in ["A","B"]:
        for endpoint in ["F","D"]:
            if (begin in graph) and (endpoint in graph):
                result_temp += bfs_find_path(graph_double, begin, endpoint, 10)


    with open("..//Data//KG//transformed_data.json", 'r') as file:
        kg = json.load(file)
    #sd = bfs_find_path(kg,"10","327",2)














