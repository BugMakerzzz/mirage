import json 
import os
import argparse
import random
from utils.config import default_objects, default_names
from prompt.instruction import instruction_dic, rule_format_dic
from generate_data import make_new_fact

context_templates = {
'symbol':"""Input: {obj_sent}\tOutput: {res_sent}
""",
'trade':"""{name} went to the market to trade items based on the rule. He originally had {obj_sent} After the trade, he had {res_sent}
""",
'diet':"""{name} adjusted his diet plan according to the expert's advice. He originally planned to take in {obj_sent} After the adjustment, he had {res_sent}
""",
'magic':"""{name} was performing a card magic trick. Initially, he had {obj_sent} After performing the magic, he ended up with {res_sent}
""",
'invest':"""{name} adjusted the investment amount of each asset according to certain criteria. Initially, he invested {obj_sent} After the adjustment, he invested {res_sent}
""",
'course':"""{name} adjusted the students' course schedule according to certain rules. Initially, the weekly course schedule was: {obj_sent} After the adjustment, the weekly course schedule was: {res_sent}
""",
'string':"""Input: {obj_sent}\tOutput: {res_sent}
""",
'code':"""f({obj_sent}) = {res_sent}
"""
}

question_templates = {
'symbol':"""Input: {obj_sent}
""",
'trade':"""{name} went to the market to trade items based on the rule. He originally had {obj_sent} What items will he have after the trade?
""",
'diet':"""{name} adjusted his diet plan according to the expert's advice. He originally planned to take in {obj_sent} What diet will he take after the adjustment?
""",
'magic':"""{name} was performing a card magic trick. Initially, he had {obj_sent} What cards will he have after performing the magic?
""",
'invest':"""{name} adjusted the investment amount of each asset according to certain criteria. Initially, he invested {obj_sent} What assets will he invest after the adjustment?
""",
'course':"""{name} adjusted the students' course schedule according to certain rules. Initially, the weekly course schedule was: {obj_sent} What will the weekly course schedule be after the adjustment?
""",
'string':"""Input: {obj_sent}
""",
'code':"""f({obj_sent}) = ?
"""
}

context_keywords = {
    'symbol': 'list transformation',
    'trade': 'trade',
    'diet': 'diet adjustment',
    'magic': 'magic',
    'invest': 'investment adjustment',
    'course': 'course adjustment',
    'string': 'string transformation',
    'code': 'function'
}


def convert_vec_to_str(vec, type, objects, explicit=False):
    if type == 'symbol':
        sent = ', '.join([str(num) for num in vec])
        sent = '[' + sent + ']'
        return sent
    elif type == 'code':
        sent = ', '.join([str(num) for num in vec])
        return sent 
    elif type == 'string':
        if isinstance(vec[0], int):
            sent = ''.join([chr(ord('a')+num) for num in vec])
        else:
            sent = ''.join(vec)
        return sent
    else:
        if type == 'diet':
            quant = ' g '
        elif type == 'invest':
            quant = ' million '
        else:
            quant = ' '
        sent = ""
        for i in range(len(vec)):
            if explicit or vec[i]:
                sent += f'{vec[i]}{quant}{objects[i]}, '
        if not sent:
            sent += "nothing, "
        sent = sent[::-1].replace(",", ".", 1)[::-1].strip()
        return sent  

def str_operate(rule, obj_vec, res_vec):
    if isinstance(obj_vec[0], int):
        vec = [chr(ord('a')+num) for num in obj_vec]
    else:
        vec = obj_vec.copy()
    op_type = rule['op_type']
    new_vec = vec.copy()
    idx = rule['op_idx']
    if op_type == 'map':
        coef = rule['config']
        for i in idx:
            if coef['b']:
                new_vec[i] = coef['f'] * f'{vec[i]}' + f"{chr(ord('a')+coef['b'])}"
            else:
                new_vec[i] = coef['f'] * f'{vec[i]}' 
    elif op_type == 'add':
        for i in range(len(new_vec)):
            new_vec[i] = "".join(vec[i].split('+'))
    elif op_type == 'pad':
        for i in idx:
            if rule['config']:
                new_vec[i] = chr(ord('a')+rule['config'])
            else:
                new_vec[i] = ""
    else:
        if isinstance(res_vec[0], int):
            res_vec = [chr(ord('a')+num) for num in res_vec]
        new_vec = res_vec
    return new_vec


if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument('--task_type', type=str, default='deductive') 
    parser.add_argument('--max_obj', type=int, default=3)
    parser.add_argument('--data_type', type=str, default='mix')
    parser.add_argument('--fact_cnt', type=int, default=5)
    parser.add_argument('--context_type', type=str, default='symbol')
    parser.add_argument('--expl', action='store_true')
    parser.add_argument('--test_cnt', type=int, default=1)
    parser.add_argument('--fix_test', action='store_true')
    parser.add_argument('--nb_level', type=int, default=0)
    parser.add_argument('--nb_type', type=str, default=None)
    parser.add_argument('--target_type', type=str, default=None)
    parser.add_argument('--cls', type=int, default=0)
    parser.add_argument('--large', action='store_true')
    parser.add_argument('--disturb', action='store_true')

    args = parser.parse_args()
    max_obj = args.max_obj
    task_type = args.task_type
    fact_cnt = args.fact_cnt
    data_type = args.data_type
    context_type = args.context_type
    explicit = args.expl
    test_cnt = args.test_cnt
    fix_test = args.fix_test
    nb_level = args.nb_level
    nb_type = args.nb_type
    target_type = args.target_type
    cls = args.cls
    large = args.large
    disturb = args.disturb
    
    abs_coefs = [chr(ord('A')+i) for i in range(max_obj)]
    data_path =  f'../data/o-{max_obj}/{data_type}/f-{fact_cnt}/filter_data'
    if large:
        data_path += '_l'
    if nb_type:
        data_path += f'_{nb_type}{nb_level}'
    if fix_test:
        data_path += '_fix'
    if cls:
        data_path += f'_cls{cls}'

    with open(data_path+'.json', 'r') as f:
        data = json.load(f)
        
    questions = []
    for item in data:
        rule = item['rule']
        facts = item['train_fact']
        if context_type == 'natural':
            type = random.choice(list(default_objects.keys()))
            rule_objs = random.sample(default_objects[type], k=max_obj)
            names = random.sample(default_names, k=fact_cnt)
        else:
            type = context_type
            rule_objs = None
            names = ['' for i in range(fact_cnt)]
        context = ""
        template = context_templates[type]
        
        if disturb:
            dis_index = random.randint(0, fact_cnt-1)
            disturb_res = make_new_fact(max_obj=max_obj)
            target_res = facts[dis_index]['res_vec']
            while disturb_res == target_res:
                disturb_res = make_new_fact(max_obj=max_obj)
            facts[dis_index]['res_vec'] = disturb_res
        for i in range(len(facts)):
            obj_sent = convert_vec_to_str(facts[i]['obj_vec'], type, rule_objs)
            if type == 'string':
                facts[i]['res_vec'] = str_operate(rule=rule, obj_vec=facts[i]['obj_vec'], res_vec=facts[i]['res_vec'])
            res_sent = convert_vec_to_str(facts[i]['res_vec'], type, rule_objs)
            sent = template.format(name=names[i], obj_sent=obj_sent, res_sent=res_sent)
            context += f"Fact {i+1}: {sent}"
        keyword = context_keywords[type]    
        obj_sent = convert_vec_to_str(abs_coefs, type, rule_objs)
        abs_sent = obj_sent
        if type == 'string':
            rule['res'] = str_operate(rule=rule, obj_vec=abs_coefs, res_vec=rule['res'])
            res_sent = convert_vec_to_str(['.' for _ in range(max_obj)], type, rule_objs)  
        else:
            res_sent = convert_vec_to_str(['<<expression>>' for _ in range(max_obj)], type, rule_objs)  
        inst_obj = obj_sent
        inst_res = res_sent
        inst_type = keyword
        for k in range(test_cnt):   
            if 'ind' in task_type: 
                label = rule['res']
                golden_res = convert_vec_to_str(label, type, rule_objs)
                golden_res = rule_format_dic[context_type].format(keyword=keyword, obj_sent=obj_sent, res_sent=golden_res)
                if task_type == 'inductive':
                    question = f'Please generate the rule of {keyword} based on the former facts.\n'
            
            if 'ded' in task_type:
                
                if target_type:
                    if target_type == 'natural':
                        type = random.choice(list(default_objects.keys()))
                        rule_objs = random.sample(default_objects[type], k=max_obj)
                        names = random.sample(default_names, k=fact_cnt)
                    else:
                        type = target_type
                    if type == 'string':
                        res_sent = convert_vec_to_str(['.' for _ in range(max_obj)], type, rule_objs)  
                    else:
                        res_sent = convert_vec_to_str(['<<expression>>' for _ in range(max_obj)], type, rule_objs)  
                    inst_res = res_sent
                query_name = random.choice([name for name in default_names if name not in names])
                # query_fact = random.choice(item['test_fact'])
                if k < len(item['test_fact']):
                    query_fact = item['test_fact'][k]
                else:
                    break
                # if task_type != 'rule_deductive':
                obj_sent = convert_vec_to_str(query_fact['obj_vec'], type, rule_objs)
                if type == 'string':
                    query_fact['res_vec'] = str_operate(rule=rule, obj_vec=query_fact['obj_vec'], res_vec=query_fact['res_vec'])
                res_sent = convert_vec_to_str(['<<expression>>' for _ in range(max_obj)], type, rule_objs)  
                question = 'Question: ' + question_templates[type].format(keyword=keyword, obj_sent=obj_sent, name=query_name)
                if task_type == 'ind_deductive':
                    label = {'rule':label, 'fact':query_fact['res_vec']}
                    answer_res = convert_vec_to_str(label['fact'], type, rule_objs)
                    answer_res = 'Answer'+ instruction_dic['deductive'].split('Answer')[-1].format(keyword=keyword, res_sent=answer_res)
                    golden_res = golden_res + '\nBased on the rule, we can infer the answer as below:\n' + answer_res
                else:
                    if task_type == 'rule_deductive':
                        rule_label = rule['res']
                        rule_sent = convert_vec_to_str(rule_label, type, rule_objs)
                        # print(obj_sent)
                        context = 'Rule'+ rule_format_dic[context_type].split('Rule')[-1].format(keyword=keyword, obj_sent=abs_sent, res_sent=rule_sent) + '\n' 
                    label = query_fact['res_vec']
                    golden_res = convert_vec_to_str(label, type, rule_objs)
                    golden_res = 'Answer'+ instruction_dic['deductive'].split('Answer')[-1].format(keyword=keyword, res_sent=golden_res)
         
            if test_cnt > 1:
                id = item['id'] + f'_T{k}'
            else:
                id = item['id']
            question = context + question 
            msg = {
                'id': id,
                'op_type': rule['op_type'],
                'objects': rule_objs,
                'context_type': type,
                'question': question,
                'label': label,
                'golden_res': golden_res,
                'inst_info':{
                    'type':inst_type,
                    'obj':inst_obj,
                    'res':inst_res
                }
            }
            questions.append(msg)
    
    question_path = f'../data/o-{max_obj}/{data_type}/f-{fact_cnt}/'
    if not os.path.exists(question_path):
        os.makedirs(question_path)
    question_path += f'{context_type}_{task_type}'
    if target_type:
        question_path += f'_{target_type}'
    if nb_type:
        question_path += f'_{nb_type}{nb_level}'
    if explicit:
        question_path += '_expl'
    if test_cnt > 1:
        question_path += f'_t{test_cnt}'
    if fix_test:
        question_path += f'_fix'
    if cls:
        question_path += f'_cls{cls}'
    if large:
        question_path += '_l'
    if disturb:
        question_path += '_dis'
    with open(question_path+'.json', 'w') as f:
        json.dump(questions, f, indent=4)