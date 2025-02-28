from utils.model import ModelWrapper
from tqdm import tqdm
import os
import argparse
import re
import json 
import numpy as np
from prompt.instruction import method_instruction_dic, rule_format_dic
from inference import match_rule, match_fact

hr_refine_question_template = """{fact}
Your rule: {rule}
This rule does not work for the following examples.
{feedback}
Generate a new rule that maps the given inputs to their corresponding outputs.
"""

sr_refine_question_template = """{fact}
Your rule: {rule}
Feedback: {feedback}
Generate a new rule.
"""

feedback_template = """{fact}
Your rule: {rule}
Generate a feedback.
"""



def hr_select_rule(model, responses, item, sample_cnt):
    rule_cor_counts = []
    fact = item['question'].split('\nQuestion')[-2]
    for i in range(sample_cnt):
        rule = responses[i]
        instruction = method_instruction_dic['hr']['feedback']
        input = [{"role": "system", "content": instruction}]
        question = feedback_template.format(fact=fact, rule=rule)
        input.append({"role": "user", "content": question})
        response = model.generate(input)[0]
        count = response.split('###')[-2].split(':')[-1].strip()
        count_pattern = r'(\d)'
        if re.match(count_pattern, count):   
            count = int(re.findall(count_pattern, count)[0])
        else:
            count = -1
        rule_cor_counts.append(count)
    idx = np.argmax(np.array(rule_cor_counts))
    return responses[idx]


def hr_update_rule(model, old_responses, item, sample_cnt):
    rule_cor_counts = []
    feedbacks = []
    fact = item['question'].split('\nQuestion')[-2]
  
    for i in range(sample_cnt):
        rule = old_responses[i]
        instruction = method_instruction_dic['hr']['feedback']
        input = [{"role": "system", "content": instruction}]
        question = feedback_template.format(fact=fact, rule=rule)
        input.append({"role": "user", "content": question})
        response = model.generate(input)[0]
        # print(response)
        count = response.split('###')[-2].split(':')[-1].strip()
        count_pattern = r'(\d)'
        if re.match(count_pattern, count):   
            count = int(re.findall(count_pattern, count)[0])
        else:
            count = -1
        feedback = response.split('###')[-1].strip()
        feedbacks.append(feedback)
        rule_cor_counts.append(count)

    idx = np.argmax(np.array(rule_cor_counts))
    # print(rule_cor_counts[idx])
    if rule_cor_counts[idx] == fact_cnt:
        print(old_responses[idx])
        return old_responses[idx], True
    feedback = feedbacks[idx]
    question = hr_refine_question_template.format(fact=fact, rule=old_responses[i], feedback=feedback)
    rule_format = rule_format_dic[context_type].format(keyword=item['inst_info']['type'], obj_sent=item['inst_info']['obj'], res_sent=item['inst_info']['res'])
    instruction = method_instruction_dic['hr']['refine'].format(rule_format=rule_format)
    input = [{"role": "system", "content": instruction}, {"role": "user", "content": question}]
    
    new_responses = model.generate(input, sample_cnt=sample_cnt)

    return new_responses, False
        
        
def sr_update_rule(model, old_responses, item, history):
    fact = item['question'].split('\nQuestion')[-2]
    rule = old_responses[0]
    instruction = method_instruction_dic['sr']['feedback']
    question = feedback_template.format(fact=fact, rule=rule)
    input = [{"role": "system", "content": instruction}, {"role": "user", "content": question}]
    history += input
    feedback = model.generate(input)[0]
    question = sr_refine_question_template.format(fact=fact, rule=rule, feedback=feedback)
    rule_format = rule_format_dic[context_type].format(keyword=item['inst_info']['type'], obj_sent=item['inst_info']['obj'], res_sent=item['inst_info']['res'])
    instruction = method_instruction_dic['hr']['refine'].format(rule_format=rule_format)
    input = [{"role": "system", "content": instruction}, {"role": "user", "content": question}]
    history += input
    
    new_responses = model.generate(history)
    return new_responses
        


if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--datalength', type=int, default=100)
    parser.add_argument('--max_obj', type=int, default=3)
    parser.add_argument('--data_type', type=str, default='mix')
    parser.add_argument('--fact_cnt', type=int, default=5)
    parser.add_argument('--context_type', type=str, default='symbol')
    parser.add_argument('--model', type=str, default='gpt-4o')
    parser.add_argument('--method', type=str, default='direct_0')
    parser.add_argument('--nb_level', type=int, default=0)
    parser.add_argument('--nb_type', type=str, default=None)
    parser.add_argument('--test_cnt', type=int, default=5)
    parser.add_argument('--sample_cnt', type=int, default=1)
    parser.add_argument('--max_iter', type=int, default=3)

    args = parser.parse_args()
    max_obj = args.max_obj
    datalength = args.datalength
    fact_cnt = args.fact_cnt
    data_type = args.data_type
    context_type = args.context_type
    model_name = args.model 
    method = args.method 
    nb_level = args.nb_level
    nb_type = args.nb_type
    sample_cnt = args.sample_cnt
    max_iter = args.max_iter
    
    ind_data_path =  f'../data/o-{max_obj}/{data_type}/f-{fact_cnt}/{context_type}_inductive'
    if nb_type:
        ind_data_path += f'_{nb_type}{nb_level}'
    with open(ind_data_path+'.json', 'r') as f:
        ind_data = json.load(f)
    
    ded_data_path =  f'../data/o-{max_obj}/{data_type}/f-{fact_cnt}/{context_type}_deductive'
    if nb_type:
        ded_data_path += f'_{nb_type}{nb_level}'
    with open(ded_data_path+'.json', 'r') as f:
        ded_data = json.load(f)
      
    model_wrapper = ModelWrapper(model_name=model_name)
    results = []
    correct = {'ind':0, 'ded':0}
    if datalength > 100:
        index = range(100, datalength)
    else:
        index = range(datalength)
    for i in tqdm(index):
        ind_item = ind_data[i]
        ded_item = ded_data[i]
        if ind_item['id'] != ded_item['id']:
            assert 'NO Alignment!'
        rule_format = rule_format_dic[context_type].format(keyword=ind_item['inst_info']['type'], obj_sent=ind_item['inst_info']['obj'], res_sent=ind_item['inst_info']['res'])
        ind_item['rule_format'] = rule_format
        iter = 0
        instruction = method_instruction_dic[method]['inductive'].format(keyword=ind_item['inst_info']['type'], rule_format=rule_format)
        input = [{"role": "system", "content": instruction}, {"role": "user", "content": ind_item['question']}]
        history = input.copy()
        responses = model_wrapper.generate(input, sample_cnt=sample_cnt)
        flag = False
        while iter < max_iter:
            if method == 'hr':
                responses, flag = hr_update_rule(model=model_wrapper, old_responses=responses, item=ded_item, sample_cnt=sample_cnt)
                if flag:
                    break
            else:
                responses = sr_update_rule(model=model_wrapper, old_responses=responses, item=ded_item, history=history)
            iter += 1
        if method == 'hr':
            if flag:
                rule = responses
            else:
                rule = hr_select_rule(model=model_wrapper, responses=responses, item=ded_item, sample_cnt=sample_cnt)
        else:
            rule = responses[0]
        ind_pred, ind_match = match_rule(rule, ind_item['label'], ind_item, context_type)
        if ind_match:
            correct['ind'] += 1

        instruction = method_instruction_dic[method]['deductive'].format(keyword=ded_item['inst_info']['type'], res_sent=ded_item['inst_info']['res'])
        question = rule + '\n' + ded_item['question']
        input = [{"role": "system", "content": instruction}, {"role": "user", "content": question}]
        response = model_wrapper.generate(input)[0]
        ded_pred, ded_match = match_fact(response, ded_item['label'], ded_item, context_type)
        
        if ded_match:
            correct['ded'] += 1
        
        result = {
            'id': ded_item['id'],
            'op_type': ded_item['op_type'],
            'context_type': ded_item['context_type'],
            'instruction': instruction,
            'question': ded_item['question'],
            'response': {'ind':rule, 'ded':response},
            'pred': {'ind':ind_pred, 'ded':ded_pred},
            'label': {'ind':ind_item['label'], 'ded':ded_item['label']},
            'match': {'ind':ind_match, 'ded':ded_match},
        }
        results.append(result)
    acc = {k: v / datalength for k, v in correct.items()}
    print(acc)
    results.append({'acc':acc})    

    result_path = f'../result/{model_name}/o-{max_obj}/{data_type}/f-{fact_cnt}/'
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    result_path += f'{method}_{context_type}'
    if nb_type:
        result_path += f'_{nb_type}{nb_level}'
    result_path += f'_it{max_iter}_sn{sample_cnt}_{datalength}'
    with open(result_path+'.json', 'w') as f:
        json.dump(results, f, indent=4)