import random 
import argparse
import os 
import json 
import numpy as np
from tqdm import tqdm 
random.seed(17)


def add(vec, op_idx, res_idx, config=None):
    if not vec:        
        return None
    ops = [vec[i] for i in op_idx]
    if not config:
        res = '+'.join(ops)
        config = 'add'
    else:
        res = int(np.array(ops).sum())
    new_vec = [res if i in res_idx else vec[i] for i in range(len(vec))]
    return new_vec, config

def pad(vec, op_idx, res_idx=None, config=None):
    if not vec:        
        return None
    if not config:
        config = random.randint(0, 9)
        new_vec = [str(config) if i in op_idx else vec[i] for i in range(len(vec))]
    else:
        new_vec = [config if i in op_idx else vec[i] for i in range(len(vec))]
    return new_vec, config

def map(vec, op_idx, res_idx=None, config=None):
    if not vec:        
        return None
    
    def create_function():
        coef = random.randint(1,9)
        bias = random.randint(0,9)
        config = {}
        config['f'] = coef 
        config['b'] = bias
        return config
    
    if not config:
        config = create_function()
        if config['b']:
            new_vec = [f"{config['f']}{vec[i]}+{config['b']}" if i in op_idx else vec[i] for i in range(len(vec))]
        else:
            new_vec = [f"{config['f']}{vec[i]}" if i in op_idx else vec[i] for i in range(len(vec))]
    else:
        new_vec = [(config['f']*vec[i]+config['b']) if i in op_idx else vec[i] for i in range(len(vec))]
    return new_vec, config

def copy(vec, op_idx, res_idx, config=None):
    assert len(op_idx) == len(res_idx), "Operator and results must have the same length!"
    if not vec:        
        return None
    if not config:
        config = 'copy'
    new_vec = vec.copy()
    for i in range(len(vec)):
        if i in res_idx:
            idx = op_idx[res_idx.index(i)]
            new_vec[i] = vec[idx]
    return new_vec, config

def swap(vec, op_idx, res_idx, config=None):
    assert len(op_idx) == len(res_idx), "Operator and results must have the same length!"
    if not vec:        
        return None
    if not config:
        config = 'swap'
    new_vec = vec.copy()
    for i in range(len(vec)):
        if i in op_idx:
            idx = res_idx[op_idx.index(i)]
            new_vec[i] = vec[idx]
        if i in res_idx:
            idx = op_idx[res_idx.index(i)]
            new_vec[i] = vec[idx]
    return new_vec, config

operate_dic = {
    'add': add,
    'pad': pad,
    'map': map,
    'copy': copy,
    'swap': swap
}

def make_new_fact(max_obj, large=False, new_fact=False):
    if large:
        max_obj = random.choice(range(max_obj, 11))
        obj_vec = [random.randint(0, 9) for _ in range(max_obj)]
    elif new_fact:
        obj_vec = [random.randint(0, 9) for _ in range(max_obj)]
    else:
        obj_cnt = random.randint(1, max_obj)
        obj_idx = random.sample(range(max_obj), k=obj_cnt)
        obj_vec = [random.randint(1, 9) if i in obj_idx else 0 for i in range(max_obj)]
    return obj_vec


def generate_rules():
    rules = []
    for _ in range(data_length):
        op_type = random.choice(list(operate_dic.keys()))
        op = operate_dic[op_type]
        op_idx_length = random.randint(1, max_obj)
        op_idx = random.sample(range(max_obj), op_idx_length)
        if op_type == 'add':
            res_idx_length = random.randint(1, max_obj)
            res_idx = random.sample(range(max_obj), res_idx_length)
        elif op_type in ['copy', 'swap']:
            res_idx = random.sample(range(max_obj), op_idx_length)
        else:
            res_idx = None
        res_vec, config = op(vec=abs_coefs, op_idx=op_idx, res_idx=res_idx)    
        rule = {
            'op_type': op_type,
            'op_idx': op_idx,
            'op': op,
            'res_idx': res_idx,
            'res': res_vec,
            'config': config
        }
        rules.append(rule)
    return rules

def generate_facts(rules):
    facts = []
    for rule in rules:
        examples = []
        op = rule['op']
        op_idx = rule['op_idx']
        res_idx = rule['res_idx']
        config = rule['config']
        for _ in range(fact_cnt):
            obj_vec = make_new_fact(max_obj=max_obj, large=large)
            res_vec, _ = op(vec=obj_vec, op_idx=op_idx, res_idx=res_idx, config=config)   
            example_msg = {
                'obj_vec': obj_vec,
                'res_vec': res_vec
            }
            examples.append(example_msg)
        facts.append(examples)
    return facts
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_length', type=int, default=50000)
    parser.add_argument('--fact_cnt', type=int, default=10)
    parser.add_argument('--max_obj', type=int, default=5)
    parser.add_argument('--large', action='store_true')

    args = parser.parse_args()
    data_length = args.data_length
    fact_cnt = args.fact_cnt
    max_obj = args.max_obj
    large = args.large

    abs_coefs = [chr(ord('A')+i) for i in range(max_obj)]


    rules = generate_rules()
    facts = generate_facts(rules)

    data = []
    for i in tqdm(range(data_length)):
        rule = rules[i]
        fact = facts[i]
        del rule['op']
        msg = {
            'rule': rule,
            'fact': fact,
        }
        data.append(msg)
    
    data_path = f'../data/o-{max_obj}/'
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    if large:
        with open(data_path+'raw_data_l.json', 'w') as f:
            json.dump(data, f, indent=4)
    else:
        with open(data_path+'raw_data.json', 'w') as f:
            json.dump(data, f, indent=4)

    