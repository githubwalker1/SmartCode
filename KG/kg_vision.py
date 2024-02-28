import streamlit
from streamlit_agraph import agraph, Node, Edge, Config
import sys
import string
import numpy as np
data_path=''

#读取数据
op=open('C:\\Users\\pp\\Desktop\\SmartCode\\KG\\kg_num','r')
list=[]
for line in op:
    list.append(line)
num=1462
subs=np.arange(num)
objs=np.arange(num)

rels = [([0] * num) for i in range(num)]
for i  in  range(0,num):
   list[i] = list[i].replace("(", "").replace(")", "")
   subs[i]= int(list[i].split(',')[0])
   objs[i] = int(list[i].split(',')[2])
a=np.unique(subs)
b=np.unique(objs)
c=np.append(a,b)
c=np.unique(c)
nodes=[]
edges=[]

for i  in  range(0,len(c)):
    nodes.append( Node( id=str(c[i]),
                        label="function",
                        size=25,
                        shape="circularImage",
                        image="http://i0.hdslb.com/bfs/article/aafceafc4edf590856866c4ed0d56d4d7a6c8635.jpg"
                  )
                ) # includes **kwargs

for i  in  range(0,num):
    edges.append(   Edge(source=str(subs[i]),
                    label=list[i].split(',')[1],
                    target=str(objs[i]),
                   # **kwargs
                   )
            )

config = Config(width=1500,
                height=1500,
                # **kwargs
                )

return_value = agraph(nodes=nodes,
                      edges=edges,
                      config=config)
