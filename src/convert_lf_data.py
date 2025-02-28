import json 
import os 
from prompt.instruction import method_instruction_dic, rule_format_dic

tasks = ['inductive','deductive']
types = ['symbol', 'natural', 'string', 'code']

dataset_info_path = '../LLaMA-Factory/data/dataset_info.json'
lf_data_dir = '../LLaMA-Factory/data/'
train_bash_dir = '../LLaMA-Factory/examples/train_lora/'

with open(dataset_info_path, 'r') as f:
    data_info = json.load(f)

for task in tasks:
    for type in types:
        raw_data_path = f'../data/o-5/mix/f-5/{type}_{task}.json'
        with open(raw_data_path, 'r') as f:
            raw_data = json.load(f)
        train_data = raw_data[200:8200]
        lf_file_name = f'{type}_{task}'
        lf_file_path = os.path.join(lf_data_dir, f'{lf_file_name}.json')
        results = []
        for item in train_data:
            rule_format = rule_format_dic[type].format(keyword=item['inst_info']['type'], obj_sent=item['inst_info']['obj'], res_sent=item['inst_info']['res'])
            instruction = method_instruction_dic['direct'][task].format(keyword=item['inst_info']['type'], rule_format=rule_format, res_sent=item['inst_info']['res']) 
            msg = {
                'instruction':instruction,
                'input':item['question'],
                'output':item['golden_res']
            }
            results.append(msg)
        with open(lf_file_path, 'w') as f:
            json.dump(results, f, indent=4)
        data_info[lf_file_name] = {'file_name':f'{lf_file_name}.json'}

with open(dataset_info_path, 'w') as f:
    json.dump(data_info, f, indent=4)