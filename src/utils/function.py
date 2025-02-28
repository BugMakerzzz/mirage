### Generate fictional objects, place, name, etc.
import random 
import json
import re
from utils.config import head_dics, f_head_dics
random.seed(17)
OR = 0
AND = 1
# load prompt
sent_prompt_path = '/mnt/userdata/ljc/code/inductive_reason/prompt/generate_sent.json'
with open(sent_prompt_path, 'r') as f:
    sent_prompt = json.load(f)



def format_prompt(full_prompt, item):
    fields = re.findall('\{\{\w+\}\}', full_prompt)
    for field in fields:
        if field[2:-2] not in item.keys():
            continue
        value = item[field[2:-2]]
        
        if type(value) == list:
            value = '\n'.join(value)
        
        full_prompt = full_prompt.replace(field, value)
         
    return full_prompt


class Object():
    def __init__(self, name):
        self.name = name
        self.father = None 
        self.children = []
        self.triples = []
    
    def get_children(self, children):
        self.children.append(children)
    
    def get_father(self, father):
        self.father = father
    
    def get_triple(self, triple):
        self.triples.append(triple)
    
    def __eq__(self, __value: object) -> bool:
        return self.name == __value.name


class Item():
    def __init__(self, triple, neg):
        self.triple = triple 
        self.neg = neg
        self.sent = self.load_sent()

    def load_sent(self):
        prompts = sent_prompt[self.triple['rel']]
        if self.neg:
            prompt = random.choice(prompts['negative'])
        else:
            prompt = random.choice(prompts['positive']) 
        sent = format_prompt(prompt, self.triple)
        return sent 
    
    def load_head(self, head):
        new_triple = self.triple.copy()
        new_triple['head'] = head
        return Item(new_triple, self.neg) 
        
class Fact():
    def __init__(self, premises, conclusions, rule) -> None:
        self.premises = premises
        self.conclusions = conclusions
        if premises:
            self.p_length = len(premises)
        else:
            self.p_length = 0
        if conclusions:
            self.c_length = len(conclusions)
        else:
            self.c_length = 0
        self.rule = rule
        self.noises = None
        # self.p_connections = []
        # self.c_connections = []
        # for i in range(self.p_length-1):
            # self.p_connections.append(random.choice([OR, AND]))
        # for i in range(self.c_length-1):
            # self.c_connections.append(random.choice([OR, AND]))
        self.sent = self.load_sent()
    
    def load_sent(self):
        if not self.rule:
            sent = 'If '
            for i in range(self.p_length):
                item = self.premises[i]
                item_sent = item.sent.strip().split('.')[0]
                if i < self.p_length - 1:
                    connection = f' and '
                    item_sent += connection
                sent += item_sent
            sent += ', then '
            for i in range(self.c_length):
                item = self.conclusions[i]
                item_sent = item.sent.strip().split('.')[0]
                if i < self.c_length - 1:
                    connection = f' and '
                    item_sent += connection
                sent += item_sent
            sent += '.'
        else:
            if self.premises:
                premise_sent = ' '.join([item.sent for item in self.premises])
            else:
                premise_sent = ""
            if self.conclusions:
                conclusion_sent = ' '.join([item.sent for item in self.conclusions])
            else:
                conclusion_sent = ""
            sent = premise_sent + " " + conclusion_sent
        return sent
    
    def set_noises(self, noises):
        self.noises = [noise.load_head('X') for noise in noises]      
        return 
        
def load_object_tree(triple):
    if triple == 'correct':
        head_dic = head_dics
    else:
        head_dic = f_head_dics
    object_tree = []
    for top_head, top_ls in head_dic.items():
        top_node = Object(top_head)
        for mid_head, mid_ls in top_ls.items():
            mid_node = Object(mid_head)
            top_node.get_children(mid_node)
            mid_node.get_father(top_node)
            for bot_head in mid_ls:
                bot_node = Object(bot_head)
                mid_node.get_children(bot_node)
                bot_node.get_father(mid_node)
            object_tree.append(mid_node)
    return object_tree


def load_triples(path, object_tree):
    with open(path, 'r') as f:
        triples = json.load(f)
    object_dic = {obj.name:obj for obj in object_tree}    
    for triple in triples:
        head = triple['head']
        rel = triple['rel']
        tail = triple['tail']
        tup = {'rel':rel, 'tail':tail}
        mid_node = object_dic[head]
        mid_node.get_triple(tup)
        for child in mid_node.children:
            child.get_triple(tup)
        mid_node.father.get_triple(tup)
    return
