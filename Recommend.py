from Agents.Recognize_Recommend import Recognize_Recommend
from utils.concept_trans import find_node_k_hop,find_graph_path,id_to_concept,concept_to_id,get_unique_concept
from utils.glove_embedding import embedding_get_id
import json
import os

os.environ['OPENAI_API_KEY'] = ''
os.environ['OPENAI_BASE_URL'] = 'https://hb.rcouyi.com/v1'

#os.environ['OPENAI_API_KEY'] = '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'

configs = {
    "conceptpath":".//Data//Glove//concept.glove.100d.npy",
    "glove_vec_path":".//Data//Glove//glove.100d.npy",
    "glove_vocab_path":".//Data//Glove//.vocab.txt"
}


def main():
    temp = Recognize_Recommend(mode="json", temperature=0.1)
    response = temp.start()
    Question_item,Recommend_item = embedding_get_id(response,conceptpath=configs["conceptpath"],glove_vec_path=configs["glove_vec_path"],glove_vocab_path=configs["glove_vocab_path"])
    #Question_item, Recommend_item = ["255","11"],["33","22","11"]
    #node_list = find_node_k_hop(Question_item+Recommend_item,3,'.//Data//KG//transformed_data.json')
    node_list = find_graph_path(Question_item,Recommend_item,data_file='.//Data//KG//transformed_data.json')
    unique_concept_id = get_unique_concept(node_list)
    id_to_concept(node_list,'.//Data//KG//id_function.json')
    id_to_concept(unique_concept_id, './/Data//KG//id_function.json')
    return node_list,unique_concept_id

if __name__ == '__main__':
    a,b = main()
    print(a)
    print(b)