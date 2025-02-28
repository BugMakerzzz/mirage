inductive_instruction = """Please summarize the rules of the {keyword} based on the given facts. 
Your reply should strictly follow the following format:
{rule_format}
""" 

deductive_instruction = """Please answer the question based on rules of the {keyword} in the given facts. 
Your reply should strictly follow the following format:
Answer: {res_sent}
""" 

rule_deductive_instruction = """Please answer the question based on the given {keyword} rule. 
Your reply should strictly follow the following format:
Answer: {res_sent}
"""

ind_deductive_instruction = """Please summarize the {keyword} rules and answer the question based on the given facts. 
Your reply should strictly follow the following format:
{rule_format}
Based on the rule, we can infer the answer as below:
Answer: {res_sent}
""" 

cot_inductive_instruction = """Please summarize the rules of the {keyword} based on the given facts. 
Your reply should strictly follow the following format:
Thought: ...
So the rule is:
{rule_format}
""" 

cot_deductive_instruction = """Please answer the question based on rules of the {keyword} in the given facts. Let's think step by step. 
Your reply should strictly follow the following format:
Thought: ...
So the answer is:
Answer: {res_sent}
""" 

sr_feedback_instruction = """Please give a feedback to the generated rule based on the given facts.
Your reply should strictly follow the following format:
Feedback: ...
"""

sr_refine_instruction = """Please refine the rule based on the feedback, input facts and dialog histories.
Your reply should strictly follow the following format:
{rule_format}
"""

hr_feedback_instruction = """Given the rule, please evaluate it on each fact to determine whether it satisfies the rule.
### Evaluation:
For Fact 1, the input are ..., after applying the rule, the output should be ..., which is consistent/inconsistent with the fact.
For Fact 2, the input are ..., after applying the rule, the output should be ..., which is consistent/inconsistent with the fact.
...
For Fact ..., the input are ..., after applying the rule, the output should be ..., which is consistent/inconsistent with the fact.

### Count: 
Correct fact counts: {INT}

### Feedback:
Wrong facts:

Fact i: Input: ...
Expected output: ...
Actual output: ...

Fact j: Input: ...
Expected output: ...
Actual output: ...

...
"""

hr_refine_instruction = """Please refine the rule based on the feedback, input facts.
Your reply should strictly follow the following format:
{rule_format}
"""


natural_rule_format = "Rule: If there are {obj_sent} After the {keyword}, there are {res_sent}"
symbol_rule_format = "Rule: {obj_sent} -> {res_sent}"
code_rule_format = """Rule: 
def f({obj_sent}):
    {obj_sent} = {res_sent}
    return {obj_sent}
"""


instruction_dic = {
    'inductive': inductive_instruction,
    'deductive': deductive_instruction,
    'rule_deductive': rule_deductive_instruction,
    'ind_deductive': ind_deductive_instruction
}

cot_instruction_dic = {
    'deductive': cot_deductive_instruction,
    'inductive': cot_inductive_instruction
}

sr_instruction_dic = {
    'inductive': inductive_instruction,
    'feedback': sr_feedback_instruction,
    'refine': sr_refine_instruction,
    'deductive': rule_deductive_instruction
}

hr_instruction_dic = {
    'inductive': inductive_instruction,
    'feedback': hr_feedback_instruction,
    'refine': hr_refine_instruction,
    'deductive': rule_deductive_instruction
}

method_instruction_dic = {
    'direct': instruction_dic,
    'cot': cot_instruction_dic,
    'sr': sr_instruction_dic,
    'hr': hr_instruction_dic
}

rule_format_dic = {
    'natural': natural_rule_format,
    'symbol': symbol_rule_format,
    'code': code_rule_format,
    'string': symbol_rule_format
}