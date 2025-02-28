#!/bin/bash
for i in 3
do
    for j in 5
    do
        for k in symbol natural code string
        do
            # python generate_few_shot_example.py --max_obj $i --fact_cnt $j --context_type $k --task_type inductive --method $1
            # python generate_few_shot_example.py --max_obj $i --fact_cnt $j --context_type $k --task_type deductive --method $1
            python generate_few_shot_example.py --max_obj $i --fact_cnt $j --context_type $k --task_type ind_deductive --method $1
        done 
    done
done