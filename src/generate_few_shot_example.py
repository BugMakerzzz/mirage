import json 
import argparse
import random
random.seed(17)
parser = argparse.ArgumentParser()
parser.add_argument('--task_type', type=str, default='inductive') 
parser.add_argument('--max_obj', type=int, default=3)
parser.add_argument('--data_type', type=str, default='mix')
parser.add_argument('--fact_cnt', type=int, default=5)
parser.add_argument('--context_type', type=str, default='symbol')
parser.add_argument('--method', type=str, default='direct')

args = parser.parse_args()
max_obj = args.max_obj
task_type = args.task_type
fact_cnt = args.fact_cnt
data_type = args.data_type
context_type = args.context_type
method = args.method


example_path = 'prompt/icl_example.json'
with open(example_path, 'r') as f:
    examples = json.load(f)


if method == 'direct':
    question_path = f'../data/o-{max_obj}/{data_type}/f-{fact_cnt}/{context_type}_{task_type}.json'
    with open(question_path, 'r') as f:
        data = random.sample(json.load(f)[100:], k=10)    
    results = []
    for item in data:
        msg = {
            'input':item['question'],
            'output':item['golden_res'],
        }
        results.append(msg)
else:
    result_path = f'../result/gpt-4/o-{max_obj}/{data_type}/f-{fact_cnt}/{method}_0_{context_type}_{task_type}_50.json'
    with open(result_path, 'r') as f:
        data = json.load(f)[:-1]  
    results = []
    for item in data:
        if item['match'][0]:
            msg = {
                'input':item['question'],
                'output':item['response'],
            }
        results.append(msg)
    results = random.sample(results, k=10)

if task_type not in examples.keys():
    examples[task_type] = {}
if method not in examples[task_type].keys():
    examples[task_type][method] = {}
if data_type not in examples[task_type][method].keys():
    examples[task_type][method][data_type] = {}
if context_type not in examples[task_type][method][data_type].keys():
    examples[task_type][method][data_type][context_type] = {}

examples[task_type][method][data_type][context_type][f'o-{max_obj}_f-{fact_cnt}'] = results

with open(example_path, 'w') as f:
    json.dump(examples, f, indent=4)