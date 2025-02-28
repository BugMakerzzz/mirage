import random 
import argparse
import os 
import json 
import numpy as np 
from tqdm import tqdm
from generate_data import operate_dic
random.seed(17)

def filter_dup_fact(item):
    if not item:
        return None 
    facts = item['fact']
    new_facts = []
    obj_vecs = []
    for fact in facts:
        vec = fact['obj_vec']
        if vec in obj_vecs:
            continue
        obj_vecs.append(vec)
        new_facts.append(fact)
    item['fact'] = new_facts
    return item 

def filter_dup_rule(item, uni_rule_ls):
    if not item:
        return None 
    rule = item['rule']
    res = rule['res']
    dup_flag = False
    for tup in uni_rule_ls:
        if res == tup['res']:
            dup_flag = True 
            break
    if dup_flag:
        item = None 
    else:
        uni_rule_ls.append(rule)   
    return item
    
def filter_unchange_fact(item):
    if not item:
        return None 
    facts = item['fact']
    unchange_cnt = 0
    new_facts = []
    for fact in facts:
        if fact['obj_vec'] == fact['res_vec']:
            unchange_cnt += 1
            if unchange_cnt > 1:
                continue
        new_facts.append(fact)
    item['fact'] = new_facts
    return item 

def filter_zero_fact(item):
    if not item:
        return None 
    facts = item['fact']
    zero_cnt = 1
    new_facts = []
    for fact in facts:
        if np.all(np.array(fact['res_vec']) == 0):
            zero_cnt += 1
            if zero_cnt > 1:
                continue
        new_facts.append(fact)
    item['fact'] = new_facts
    return item 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_obj', type=int, default=3)
    parser.add_argument('--fact_cnt', type=int, default=5)
    parser.add_argument('--data_type', type=str, default='all')
    parser.add_argument('--fix_test',  action='store_true')
    parser.add_argument('--large',  action='store_true')

    args = parser.parse_args()
    max_obj = args.max_obj
    data_type = args.data_type
    fact_cnt = args.fact_cnt
    fix_test = args.fix_test
    large = args.large

    raw_data_path = f'../data/o-{max_obj}/raw_data'
    if large:
        raw_data_path += '_l'
    with open(raw_data_path+'.json', 'r') as f:
        raw_data = json.load(f)

    data = {op_type:[] for op_type in operate_dic.keys()}
    mix_data = []
    uni_rule_ls = []
    idx = -1
    for item in tqdm(raw_data):
        item = filter_dup_fact(item)
        item = filter_zero_fact(item)
        item = filter_unchange_fact(item)
        item = filter_dup_rule(item, uni_rule_ls)
        if item:
            idx += 1
            id = f'O{max_obj}_{idx}'
            if len(item['fact']) <= fact_cnt:
                continue
            if fix_test:
                test_fact = item['fact'][:-fact_cnt]
                train_fact = item['fact'][-fact_cnt:]
            else:
                train_fact = random.sample(item['fact'], k=fact_cnt)
                test_fact = [fact for fact in item['fact'] if fact not in train_fact]
            item['train_fact'] = train_fact
            item['test_fact'] = test_fact
            del item['fact']
            item['id'] = id
            data[item['rule']['op_type']].append(item)
            mix_data.append(item)
 
    if data_type == 'all':   
        for op_type, type_data in data.items():
            data_path = f'../data/o-{max_obj}/{op_type}/f-{fact_cnt}/'
            if not os.path.exists(data_path):
                os.makedirs(data_path)
            data_path += 'filter_data'
            if fix_test:
                data_path += '_fix'
            if large:
                data_path += '_l'
            with open(data_path+'.json', 'w') as f:
                json.dump(type_data, f, indent=4)              
    if data_type == 'all' or data_type == 'mix':
        data_path = f'../data/o-{max_obj}/mix/f-{fact_cnt}/'
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        data_path += 'filter_data'
        if fix_test:
            data_path += '_fix'
        if large:
            data_path += '_l'
        with open(data_path+'.json', 'w') as f:
            json.dump(mix_data, f, indent=4)
    else:
        type_data = data[data_type]
        data_path = f'../data/o-{max_obj}/{data_type}/f-{fact_cnt}'
        if not os.path.exists(data_path):
            os.makedirs(data_path)
        data_path += 'filter_data'
        if fix_test:
            data_path += '_fix'
        if large:
            data_path += '_l'
        with open(data_path+'.json', 'w') as f:
            json.dump(type_data, f, indent=4)