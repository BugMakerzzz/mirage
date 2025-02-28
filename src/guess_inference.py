from utils.model import ModelWrapper
from tqdm import tqdm
import os
import argparse
import re
import json 
from prompt.instruction import method_instruction_dic, rule_format_dic

def normalize_expression(expression):
    expression = re.sub(r'\(?([1-9])\s?\*\s?([A-Z])\)?', r'\1\2', expression)
    expression = re.sub(r'\(?([A-Z])\s?\*\s?([1-9])\)?', r'\2\1', expression)
    return expression
 
def sort_expression(vec):
    sorted_vec = []
    for exp in vec:
        parts = exp.split('+')
        sorted_parts = sorted(parts)
        sorted_expression = '+'.join(sorted_parts)
        sorted_vec.append(sorted_expression)
    return sorted_vec

def norm_coef(vec):
    norm_vec = []
    for exp in vec:
        exp = re.sub(r'1([A-Z])', r'\1', exp)
        norm_vec.append(exp)
    return norm_vec
        
def match_rule(response, label, item, context_type):
    if context_type == 'code':
        pattern = r'=\s*(.*)'    
        matches = re.findall(pattern, response) 
        if matches:
            response = normalize_expression(matches[0])
        else:
            return None, False    
    else:
        matches = re.findall(r'Rule: .*', response)
        if matches:
            response = matches[-1]
            if context_type == 'natural':
                response = normalize_expression(response.split('After')[-1])
            elif context_type == 'string':
                response = response.split('->')[-1].strip()
            else:
                response = normalize_expression(response.split('->')[-1])
        else:
            return None, False  
        
    if context_type == 'string':
        pattern = r'([A-Za-z]+)\b'     
        matches = re.findall(pattern, response)
        if matches:
            pred = matches[-1]
        else:
            pred = ""
        label = ''.join(label)
    else: 
        pattern = r'((?:(?:[1-9]?[A-Z])|[0-9])(?:\s*[+-]\s*(?:(?:[1-9]?[A-Z])|\d))*)\b'     
        matches = re.findall(pattern, response)
        if matches:
            pred = [exp.replace(' ', '') for exp in matches]
            pred = [exp.replace('\u202f', '') for exp in pred]
            if item['op_type'] == 'add':
                pred = sort_expression(pred)
                label = sort_expression(label)
            elif item['op_type'] == 'map':
                pred = norm_coef(pred)
                label = norm_coef(label)
        else:
            pred = None
            
    match = (pred == label)
    return pred, match

def match_fact(response, label, item, context_type):
    matches = re.findall(r'Answer: .*', response)
    if matches:
        response = matches[-1]
    else:
        return None, False
    
    if context_type == 'string':
        pattern = r'([a-z]+)\b'
        matches = re.findall(pattern, response)
        pred = matches[-1]
        label = ''.join(label)
    else: 
        pattern = r'([0-9]+)\b' 
        if context_type == 'natural':
            pred = []
            pred_ls = response.split(',')
            for obj in item['objects']:
                cnt = 0
                for s in pred_ls:
                    if obj in s or obj.rstrip('s') in s:
                        matches = re.findall(pattern, s)
                        if matches:
                            cnt = int(matches[0])
                        break
                pred.append(cnt)
        else:
            matches = re.findall(pattern, response)
            pred = [] 
            pred = [int(exp) for exp in matches]
    match = (pred == label)
    return pred, match

  
if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--task_type', type=str, default='deductive') 
    parser.add_argument('--datalength', type=int, default=100)
    parser.add_argument('--max_obj', type=int, default=3)
    parser.add_argument('--data_type', type=str, default='mix')
    parser.add_argument('--fact_cnt', type=int, default=5)
    parser.add_argument('--context_type', type=str, default='symbol')
    parser.add_argument('--model', type=str, default='gpt-4o')
    parser.add_argument('--method', type=str, default='direct_0')
    parser.add_argument('--target_type', type=str, default=None)
    parser.add_argument('--large', action='store_true')

    args = parser.parse_args()
    max_obj = args.max_obj
    datalength = args.datalength
    task_type = args.task_type
    fact_cnt = args.fact_cnt
    data_type = args.data_type
    context_type = args.context_type
    model_name = args.model 
    method = args.method 
    target_type = args.target_type
    sample_cnt = args.sample_cnt
    large = args.large
    
    method_name, example_cnt = method.split('_')
    example_path = 'prompt/icl_example.json'
    if target_type:
        type = target_type
    else:
        type = context_type
    with open(example_path, 'r') as f:
        try:
            examples = json.load(f)[task_type][method_name][data_type][type][f'o-{max_obj}_f-{fact_cnt}'][:int(example_cnt)]
        except:
            examples = []
    model_wrapper = ModelWrapper(model_name=model_name)
    results = []
    correct = [0]
    # if datalength > 100:
    #     data = data[100:datalength]
    # else:
    data = data[:datalength]
    for item in tqdm(data):
        question = item['question']
        rule_format = "Rule: [A, B, C] -> [<<expression>>, <<expression>>, <<expression>>]"
        instruction = method_instruction_dic[method_name][task_type].format(keyword='list transformationo', rule_format=rule_format, res_sent="[<<expression>>, <<expression>>, <<expression>>]")
        if model_wrapper.is_chat:
            input = [
                {"role": "system", "content": instruction},
            ]
            for example in examples:
                input.append({"role": "user", "content":example['input']})
                input.append({"role": "assistant", "content":example['output']})
            input.append({"role": "user", "content": question})
        else:
            input = f"{instruction}\n"
            for example in examples:
                input += f"{example['input']}{example['output']}\n"
            input += question
        responses = model_wrapper.generate(input, sample_cnt=sample_cnt)
        preds = []
        matchs = []
        for i in range(sample_cnt):
            if 'ind' in task_type:
                if task_type == 'inductive':
                    pred, match = match_rule(responses[i], item['label'], item, type)
                else:
                    pred, match = match_rule(responses[i], item['label']['rule'], item, type)
                    rule_pred = pred
                    rule_match = match
            if 'ded' in task_type:
                if task_type in ['deductive', 'rule_deductive']:
                    pred, match = match_fact(responses[i], item['label'], item, type)
                else:
                    pred, match = match_fact(responses[i], item['label']['fact'], item, type)
                    pred = {'rule': rule_pred, 'fact': pred}
                    match = {'rule': rule_match, 'fact': match}
            
            if task_type == 'ind_deductive':
                if match['rule']:
                    correct['ind'][i] += 1
                if match['fact']:
                    correct['ded'][i] += 1
                if match['rule'] and match['fact']:
                    correct['both'][i] += 1
            else:
                if match:
                    correct[i] += 1
                    
            preds.append(pred)
            matchs.append(match)

        result = {
            'id': item['id'],
            'op_type': item['op_type'],
            'context_type': item['context_type'],
            'instruction': instruction,
            'question': question,
            'response': responses,
            'pred': preds,
            'label': item['label'],
            'match': matchs
        }
        results.append(result)
    if task_type == 'ind_deductive':
        acc = {}
        for k, v in correct.items():
            acc[k] = [cor / datalength for cor in correct[k]]
    else:
        acc = [cor / datalength for cor in correct]
    print(acc)
    results.append({'acc':acc})    

    result_path = f'../result/{model_name}/o-{max_obj}/{data_type}/f-{fact_cnt}/'
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    result_path += f'{method}_{context_type}_{task_type}'
    if target_type:
        result_path += f'_{target_type}'
    if nb_type:
        result_path += f'_{nb_type}{nb_level}'
    result_path += f'_{datalength}'
    if explicit:
        result_path += '_expl'
    if fix_test:
        result_path += '_fix'
    if sample_cnt > 1:
        result_path += '_sn5'
    if large:
        result_path += '_l'

    with open(result_path+'.json', 'w') as f:
        json.dump(results, f, indent=4)