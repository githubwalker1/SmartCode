import numpy as np
from numpy.linalg import norm
import json
import tqdm


def weighted_average(avg, new, n):
    # TODO: maybe a better name for this function?
    return ((n - 1) / n) * avg + (new / n)


def max_pooling(old, new):
    # TODO: maybe a better name for this function?
    return np.maximum(old, new)


def create_embeddings_glove(original_data:list, pooling="avg", dim=100,glove_vec_path="..//Data//Glove//glove.100d.npy", glove_vocab_path="..//Data//Glove//.vocab.txt"):
    '''
    :param original_data: need embedding list
    :param pooling: method
    :param dim:
    :return: 生成embedding
    '''
    glove_embeddings = load_glove_from_npy(glove_vec_path,glove_vocab_path)
    concept_embeddings = {}
    concept_embeddings_cnt = {}
    for i in range(len(original_data)):
        data = original_data[i]
        words = data.strip().split(" ")
        words_lower = [word.lower() for word in words]  # 将每个单词转换为小写
        subj = " ".join(words_lower)  # 连接转换后的单词

        # counting the frequency (only used for the avg pooling)
        # if subj not in concept_embeddings:
        #     concept_embeddings[subj] = np.zeros((dim,))
        #     concept_embeddings_cnt[subj] = 0
        # concept_embeddings_cnt[subj] += 1

        if pooling == "avg":
            subj_encoding_sum = sum([glove_embeddings.get(word, np.zeros((dim,))) for word in subj])
            subj_len = len(subj.strip().split(" "))
            subj_encoding = subj_encoding_sum / subj_len

            concept_embeddings[subj] = subj_encoding


        elif pooling == "max":
            subj_encoding = np.amax([glove_embeddings.get(word, np.zeros((dim,))) for word in words], axis=0)
            concept_embeddings[subj] = max_pooling(concept_embeddings[subj], subj_encoding)

    return concept_embeddings


def load_glove_from_npy(glove_vec_path="..//Data//Glove//glove.100d.npy", glove_vocab_path="..//Data//Glove//.vocab.txt"):
    vectors = np.load(glove_vec_path)
    with open(glove_vocab_path, "r", encoding="utf8") as f:
        vocab = [l.strip() for l in f.readlines()]

    assert (len(vectors) == len(vocab))

    glove_embeddings = {}
    for i in range(0, len(vectors)):
        glove_embeddings[vocab[i]] = vectors[i]
    #print("Read " + str(len(glove_embeddings)) + " glove vectors.")
    return glove_embeddings


def glove_init(input, output, concept_file):
    '''
    :param input:
    :param output:
    :param concept_file:
    :return: 转换为npy格式
    '''
    embeddings_file = output + '.npy'
    vocabulary_file = output.split('.')[0] + '.vocab.txt'
    output_dir = '/'.join(output.split('/')[:-1])
    output_prefix = output.split('/')[-1]

    words = []
    vectors = []
    vocab_exist = True  # check_file(vocabulary_file)
    print("loading embedding")
    with open(input, 'rb') as f:
        for line in f:
            fields = line.split()
            if len(fields) <= 2:
                continue
            if not vocab_exist:
                word = fields[0].decode('utf-8')
                words.append(word)
            vector = np.fromiter((float(x) for x in fields[1:]),
                                 dtype=np.float)

            vectors.append(vector)
        dim = vector.shape[0]
    print("converting")
    matrix = np.array(vectors, dtype="float32")
    print("writing")
    np.save(embeddings_file, matrix)
    text = '\n'.join(words)
    if not vocab_exist:
        with open(vocabulary_file, 'wb') as f:
            f.write(text.encode('utf-8'))

def cosine_similarity(vec1, vec2):
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    # 检查两个向量的范数是否为零
    if norm_vec1 == 0 or norm_vec2 == 0:
        return np.nan  # 或者选择返回其他合适的值

    dot_product = np.dot(vec1, vec2)
    return dot_product / (norm_vec1 * norm_vec2)


def findrelated_k_max(objvec, conceptpath="..//Data//Glove//concept.glove.100d.npy",threshold=0.5,kmax=5):
    '''
    :param objvec:
    :param conceptpath:
    :param threshold:
    :param kmax:
    :return: [kg_id],  ##[similarity]
    '''
    conceptglove = np.load(conceptpath)
    similarities = np.array([cosine_similarity(objvec, vec) for vec in conceptglove])

    # 获取满足阈值要求的余弦相似度及其索引
    valid_indices = np.where(similarities >= threshold)[0]
    valid_similarities = similarities[valid_indices]

    # 如果没有满足阈值的相似度，返回空列表
    if len(valid_similarities) == 0:
        return None

    # 对满足阈值的相似度进行排序，取前k个
    sorted_indices = np.argsort(valid_similarities)[::-1][:kmax]
    top_k_indices = valid_indices[sorted_indices]
    top_k_values = valid_similarities[sorted_indices]

    #return top_k_indices, top_k_values
    return top_k_indices[0]


def embedding_get_id(json_data:json,conceptpath="..//Data//Glove//concept.glove.100d.npy",glove_vec_path="..//Data//Glove//glove.100d.npy", glove_vocab_path="..//Data//Glove//.vocab.txt"):
    function_list = json_data['function']
    recommend_list = json_data["recommend"]

    function_list = create_embeddings_glove(function_list,glove_vec_path=glove_vec_path,glove_vocab_path=glove_vocab_path)
    recommend_list = create_embeddings_glove(recommend_list,glove_vec_path=glove_vec_path,glove_vocab_path=glove_vocab_path)

    function_embedding_list = [findrelated_k_max(function_list[i],conceptpath) for i in function_list]
    recommend_embedding_list = [findrelated_k_max(recommend_list[i],conceptpath) for i in recommend_list]

    function_embedding_list = list(map(str,function_embedding_list))
    recommend_embedding_list = list(map(str, recommend_embedding_list))
    return function_embedding_list,recommend_embedding_list


if __name__ == "__main__":
    json_data = {
        'function': ['open', 'readlines', 'split', 'len'],
        'recommend': ['file handling in Python', 'string manipulation in Python', 'handling file paths in Python']
    }

    # 提取 'function' 键的值
    function_list = json_data['function']
    function_list += json_data["recommend"]
    glove_embeddings = load_glove_from_npy("..//Data//Glove//glove.100d.npy", "..//Data//Glove//.vocab.txt")
    temp = create_embeddings_glove(function_list)
    objec123 = temp['open']
    top_k_indices=findrelated_k_max(objec123)

    a,b = embedding_get_id(json_data)
