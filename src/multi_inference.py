from utils.model import ModelWrapper
from tqdm import tqdm
from prompt.instruction import method_instruction_dic, rule_format_dic
from inference import match_fact, match_rule
import os
import argparse
import re
import json 

def normalize_expression(expression):
    expression = re.sub(r'\(?([1-9])\*([A-Z])\)?', r'\1\2', expression)
    expression = re.sub(r'\(?([A-Z])\*([1-9])\)?', r'\2\1', expression)
    return expression
    
def sort_expression(vec):
    sorted_vec = []
    for exp in vec:
        parts = exp.split('+')
        sorted_parts = sorted(parts)
        sorted_expression = '+'.join(sorted_parts)
        sorted_vec.append(sorted_expression)
    return sorted_vec
  
if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--task_type', type=str, default='deductive') 
    parser.add_argument('--datalength', type=int, default=100)
    parser.add_argument('--max_obj', type=int, default=3)
    parser.add_argument('--data_type', type=str, default='mix')
    parser.add_argument('--fact_cnt', type=int, default=5)
    parser.add_argument('--context_type', type=str, default='symbol')
    parser.add_argument('--model', type=str, default='Llama3_8b_chat')
    parser.add_argument('--method', type=str, default='direct_0')
    parser.add_argument('--expl', action='store_true')
    parser.add_argument('--test_cnt', type=int, default=5)
    parser.add_argument('--fix_test', action='store_true')
    parser.add_argument('--cls', type=int, default=0)
    parser.add_argument('--nb_level', type=int, default=0)
    parser.add_argument('--nb_type', type=str, default=None)

    args = parser.parse_args()
    max_obj = args.max_obj
    datalength = args.datalength
    task_type = args.task_type
    fact_cnt = args.fact_cnt
    data_type = args.data_type
    context_type = args.context_type
    model_name = args.model 
    method = args.method 
    explicit = args.expl
    test_cnt = args.test_cnt
    fix_test = args.fix_test
    nb_type = args.nb_type
    cls= args.cls
    nb_level = args.nb_level
    
    data_path =  f'../data/o-{max_obj}/{data_type}/f-{fact_cnt}/{context_type}_{task_type}'
    if nb_type:
        data_path += f'_{nb_type}{nb_level}'
    if explicit:
        data_path += '_expl'
    if test_cnt > 1:
        data_path += f'_t{test_cnt}'
    if fix_test:
        data_path += f'_fix'
    if cls:
        data_path += f'_cls{cls}'
    with open(data_path+'.json', 'r') as f:
        data = json.load(f)
    method_name, example_cnt = method.split('_')
    example_path = 'prompt/icl_example.json'
    with open(example_path, 'r') as f:
        examples = json.load(f)[task_type][method_name][data_type][context_type][f'o-{max_obj}_f-{fact_cnt}'][:eval(example_cnt)]
    
    model_wrapper = ModelWrapper(model_name=model_name)
    results = []
    result_dic = {}
    cnt = 0
    i = 0
    with tqdm(total=datalength) as pbar:
        while cnt < datalength:
            item = data[i]
            id = item['id']
            id = ('_').join(id.split('_')[:-1])
            question = item['question']
            rule_format = rule_format_dic[context_type].format(keyword=item['inst_info']['type'], obj_sent=item['inst_info']['obj'], res_sent=item['inst_info']['res'])
            instruction = method_instruction_dic[method_name][task_type].format(keyword=item['inst_info']['type'], rule_format=rule_format, res_sent=item['inst_info']['res'])
      
            if not result_dic or id != result_dic['id']:
                if result_dic and len(result_dic['match']) == test_cnt:
                    results.append(result_dic)
                    cnt += 1
                    pbar.update(1)
                if cnt == datalength:
                    break
                result_dic = {
                    'id': id,
                    'instruction': instruction,
                    'op_type': item['op_type'],
                    'context_type': item['context_type'],
                    'question': [],
                    'response': [],
                    'pred': [],
                    'label': [],
                    'match': []
                }
            
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
            response = model_wrapper.generate(input)[0]

            # for j in range(3):
            if task_type == 'ind_deductive':
                rule_pred, rule_match = match_rule(response, item['label']['rule'], item, context_type)
                fact_pred, fact_match = match_fact(response, item['label']['fact'], item, context_type)
                pred = {'rule':rule_pred, 'fact':fact_pred}
                match = fact_match
            else:
                pred, match = match_fact(response, item['label'], item, context_type)
            # if matchs.count(True) >= 2:
            #     match = True
            # else:
            #     match = False
            result_dic['question'].append(question)
            result_dic['response'].append(response)
            result_dic['pred'].append(pred)
            result_dic['label'].append(item['label'])
            result_dic['match'].append(match)
            i += 1
    raw_acc = 0
    task_acc = 0
    for dic in results:
        acc = dic['match'].count(True) / test_cnt
        raw_acc += acc
        if dic['match'].count(True) == test_cnt:
            task_acc += 1
    raw_acc /= datalength
    task_acc /= datalength
    results.append({'raw_acc':raw_acc, 'task_acc':task_acc})
    print(results[-1])
    result_path = f'../result/{model_name}/o-{max_obj}/{data_type}/f-{fact_cnt}/'
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    
    result_path += f'{method}_{context_type}_{task_type}'
    if nb_type:
        result_path += f'_{nb_type}{nb_level}'
    result_path += f'_{datalength}'
    if explicit:
        result_path += '_expl'
    if test_cnt > 1:
        result_path += f'_t{test_cnt}'
    if fix_test:
        result_path += f'_fix'
    if cls:
        result_path += f'_cls{cls}'
    with open(result_path+'.json', 'w') as f:
        json.dump(results, f, indent=4)
    