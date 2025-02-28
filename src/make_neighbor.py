import json 
import argparse
import random 
import numpy as np
from tqdm import tqdm
from generate_data import operate_dic, make_new_fact
from scipy.spatial import distance
random.seed(17)


def check_distance(test_vec, train_vec, nb_level, type='euc'):
    if type == 'euc':
        dist = distance.euclidean(test_vec, train_vec)
    elif type == 'man':
        dist = distance.cityblock(test_vec, train_vec)
    else:
        dist = distance.minkowski(test_vec, train_vec, p=3)
    return dist <= nb_level

def check_neighbor(test_vec, train_vec, nb_level, type=None):
    if type:
        return check_distance(test_vec, train_vec, nb_level, type)
    max_idx = min(len(test_vec), len(train_vec))
    for i in range(max_idx):
        if abs(test_vec[i] - train_vec[i]) <= nb_level:
            return True
    return False


def check_indomain(test_vec, train_vec, nb_level):
    max_diff = - 1
    max_idx = min(len(test_vec), len(train_vec))
    for i in range(max_idx):
        diff = abs(test_vec[i] - train_vec[i])
        if diff > max_diff:
            max_diff = diff
    return max_diff <= nb_level

def make_indomain_fact(test_vec, nb_level, large=False):
    new_vec = []
    for num in test_vec:
        start = max(0, num-nb_level)
        new_num = random.choice(range(start, num+nb_level+1))
        new_vec.append(new_num)
    if large:
        append_vec = [random.randint(1, 9) for _ in range(10)]
        rand_idx = random.choice(range(max_obj, 11))
        new_vec = (new_vec + append_vec)[:rand_idx]
    return new_vec 

def generate_vectors_around_mean(mean_vector, std_dev, num_vectors):

    # 获取向量的维度
    vector_dim = len(mean_vector)
    
    # 生成偏移量
    offsets = np.random.normal(0, std_dev, (num_vectors, vector_dim))
    vectors = np.clip(mean_vector + offsets, 0, None)  # 确保非负
    vectors = np.floor(vectors).astype(int)  # 转换为整数
    # 生成最终向量
    return vectors.tolist()


def are_vectors_unique_and_different_from_mean(vectors, mean_vector):
    """
    检查生成的所有向量是否都不同且与给定的平均向量不同。
    
    :param vectors: 生成的向量列表
    :param mean_vector: 给定的平均向量
    :return: 布尔值，表示向量是否都不同且与平均向量不同
    """
    if large:
        return True
    # 将向量转换为元组，以便可以存入集合中进行唯一性检查
    vector_tuples = [tuple(vec) for vec in vectors]
    
    # 检查所有向量是否唯一
    all_unique = len(vector_tuples) == len(set(vector_tuples))
    
    # 检查是否与平均向量不同
    different_from_mean = all(not np.array_equal(vec, mean_vector) for vec in vectors)
    
    # 返回两者的逻辑与
    return all_unique and different_from_mean



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_obj', type=int, default=3)
    parser.add_argument('--fact_cnt', type=int, default=5)
    parser.add_argument('--data_type', type=str, default='mix')
    parser.add_argument('--fix_test', action='store_true')
    parser.add_argument('--nb_type', type=str, default=None)
    parser.add_argument('--nb_level', type=int, default=None)
    parser.add_argument('--cls', type=int, default=None)
    parser.add_argument('--large', action='store_true')

    args = parser.parse_args()
    max_obj = args.max_obj
    data_type = args.data_type
    fact_cnt = args.fact_cnt
    fix_test = args.fix_test
    cls = args.cls
    nb_level = args.nb_level
    nb_type = args.nb_type
    large = args.large
        
    data_path = f'../data/o-{max_obj}/{data_type}/f-{fact_cnt}/'
    data_path += 'filter_data'
    if fix_test:
        data_path += '_fix'
    if large:
        data_path += '_l'
    with open(data_path+'.json', 'r') as f:
        data = json.load(f)

    result = []
    for item in tqdm(data):
        op_type = item['rule']['op_type']
        op_config = item['rule']['config']
        op_idx = item['rule']['op_idx']
        res_idx = item['rule']['res_idx']
        test_vec = item['test_fact'][0]['obj_vec']
        new_train_vecs = [tup['obj_vec'] for tup in item['train_fact']]
        if nb_type:
            jump_flag = False
            if '_' in nb_type:
                dis_type = nb_type.split('_')[0]
            else:
                dis_type = None 
            for i in range(fact_cnt):
                new_vec = new_train_vecs[i]
                if nb_type == 'if':
                    new_vec = make_indomain_fact(test_vec=test_vec, nb_level=nb_level)
                    new_train_vecs[i] = new_vec
                    while not are_vectors_unique_and_different_from_mean(new_train_vecs[:i+1], test_vec):
                        new_vec = make_indomain_fact(test_vec=test_vec, nb_level=nb_level)
                        new_train_vecs[i] = new_vec
                elif nb_type == 'cf':
                    if check_neighbor(test_vec=test_vec, train_vec=new_vec, nb_level=nb_level, type=dis_type) and not check_indomain(test_vec=test_vec, train_vec=new_vec, nb_level=nb_level):
                        continue
                    while not check_neighbor(test_vec=test_vec, train_vec=new_vec, nb_level=nb_level, type=dis_type) or new_vec in new_train_vecs+[test_vec] or check_indomain(test_vec=test_vec, train_vec=new_vec, nb_level=nb_level):
                        new_vec = make_new_fact(max_obj=max_obj, new_fact=True, large=large)
                else:
                    if not check_neighbor(test_vec=test_vec, train_vec=new_vec, nb_level=nb_level, type=dis_type):
                        continue
                    max_cnt = 10000
                    cnt = 0
                    while check_neighbor(test_vec=test_vec, train_vec=new_vec, nb_level=nb_level, type=dis_type) or new_vec in new_train_vecs:
                        new_vec = make_new_fact(max_obj=max_obj, new_fact=True, large=large)
                        cnt += 1
                        if cnt > max_cnt:
                            jump_flag = True 
                            break
                if jump_flag:
                    break
                new_train_vecs[i] = new_vec
                new_res, _ = operate_dic[op_type](new_vec, op_idx, res_idx, op_config)
                fact = {'obj_vec':new_vec, 'res_vec':new_res}
                item['train_fact'][i] = fact
           
        if cls:
           
            new_test_vecs = [None] * 5
            for i in range(5):
                new_vec = make_indomain_fact(test_vec=test_vec, nb_level=cls)
                new_test_vecs[i] = new_vec
                while not are_vectors_unique_and_different_from_mean(new_train_vecs+new_test_vecs[:i+1], [-1]*max_obj):
                    new_vec = make_indomain_fact(test_vec=test_vec, nb_level=cls)
                    new_test_vecs[i] = new_vec
            item['test_fact'] = []
            for i in range(5):
                new_vec = new_test_vecs[i]
                new_res, _ = operate_dic[op_type](new_vec, op_idx, res_idx, op_config)
                fact = {'obj_vec':new_vec, 'res_vec':new_res}
                item['test_fact'].append(fact)
        result.append(item)
    
    result_path = data_path 
    if nb_type:
        result_path += f'_{nb_type}{nb_level}'
    if fix_test:
        result_path += '_fix'
    if cls:
        result_path += f'_cls{cls}'
    with open(result_path+'.json', 'w') as f:
        json.dump(result, f, indent=4)