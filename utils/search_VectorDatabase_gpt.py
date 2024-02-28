from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
import openai
import os
import time
import logging
# 设置日志级别为ERROR，只显示错误消息
logging.basicConfig(level=logging.ERROR)
os.environ['OPENAI_API_KEY'] = 'sk-Rw6PwT9JEa6uRGzt687414F8163a44EbA274C383C5A4F9Fd'
os.environ['OPENAI_BASE_URL'] = 'https://hb.rcouyi.com/v1'
# os.environ['OPENAI_API_KEY'] = "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"


def prepare():
    embeddings = OpenAIEmbeddings()
    loader = TextLoader('..//Data//EmbeddingDB//DB_des//root-directory',autodetect_encoding = True)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs_1 = text_splitter.split_documents(documents)

    documents_l = []
    text_splitter = CharacterTextSplitter(
        separator = "\n\n",
        chunk_size = 100,
        chunk_overlap=0,
    )
    for i in range(7):
        loader = TextLoader(f'..//Data//EmbeddingDB//DB_des//two-directory//{i+1}_chapter//{i+1}_chapter_main.txt',autodetect_encoding = True)
        documents = loader.load()
        docs_2 = text_splitter.split_documents(documents)
        documents_l.append(docs_2)

def get_position_book(query):
    prepare()
    vectordb = Chroma(persist_directory=f'..//Data//EmbeddingDB//DB', embedding_function=embeddings)
    # 带分数的查询（对一级向量数据库查询），返回一个分数最高的
    result = vectordb.similarity_search_with_score(query, k=1)

    doc_indices = []
    for i in result:
        temp, _ = i
        doc_indices.append(docs_1.index(temp)+1)

    vectordb_l = []
    for i in range(1, 8):
        vectordb = Chroma(persist_directory=f'..//Data//EmbeddingDB//DB_2//DB_{i}C', embedding_function=embeddings)
        vectordb_l.append(vectordb)

    # 开始查询二级向量数据库
    doc_indices_end = []
    doc_indices_temp = []
    for i in doc_indices:
        result = vectordb_l[i - 1].similarity_search_with_score(query, k=2)
        for j in result:
            temp, _ = j
            doc_indices_temp.append(documents_l[i - 1].index(temp) + 1)

    # 可以定位到书中的二级标题
    doc_indices_end = []
    for i in range(len(doc_indices)):
        x = doc_indices[i]
        y = doc_indices_temp[(i) * 2]
        y1 = doc_indices_temp[(i) * 2 + 1]
        doc_indices_end.append(f'{x}.{y}')
        doc_indices_end.append(f'{x}.{y1}')
    # 将字符串列表转换为浮点数列表，并进行排序
    doc_indices_end = sorted([float(i) for i in doc_indices_end])
    doc_indices_end = [str(x) for x in doc_indices_end]
    return doc_indices_end


