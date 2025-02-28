#!/bin/bash
# python refine_inference.py --model $1 --method hr --context_type symbol --sample_cnt 5
for type in code string
do
    python inference.py --model $1 --method direct_0 --task_type ind_deductive --context_type $type --datalength 100

    python inference.py --model $1 --method direct_5 --task_type inductive --context_type $type --datalength 100
    python inference.py --model $1 --method direct_5 --task_type deductive --context_type $type --datalength 100
    python inference.py --model $1 --method direct_5 --task_type ind_deductive --context_type $type --datalength 100

    python inference.py --model $1 --dmethod cot_0 --task_type inductive --context_type $type --datalength 100 --sample_cnt 5
    python inference.py --model $1 --method cot_0 --task_type deductive --context_type $type  --datalength 100 --sample_cnt 5
    python inference.py --model $1 --method cot_5 --task_type inductive --context_type $type --datalength 100 
    python inference.py --model $1 --method cot_5 --task_type deductive --context_type $type --datalength 100


    python refine_inference.py --model $1 --method sr --context_type $type --sample_cnt 1 --datalength 100
    python refine_inference.py --model $1 --method hr --context_type $type --sample_cnt 1 --datalength 100
    # python refine_inference.py --model $1 --method hr --context_type $type --sample_cnt 5 --datalength 100
done 
for type in natural
do
    python inference.py --model $1 --method cot_0 --task_type deductive --context_type $type  --datalength 100 --sample_cnt 5
    python inference.py --model $1 --method cot_5 --task_type inductive --context_type $type --datalength 100 
    python inference.py --model $1 --method cot_5 --task_type deductive --context_type $type --datalength 100


    python refine_inference.py --model $1 --method sr --context_type $type --sample_cnt 1 --datalength 100
    python refine_inference.py --model $1 --method hr --context_type $type --sample_cnt 1 --datalength 100
    # python refine_inference.py --model $1 --method hr --context_type $type --sample_cnt 5 --datalength 100
done 
