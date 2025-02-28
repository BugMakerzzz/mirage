#!/bin/bash
for i in 3
do
    for j in 5
    do
        for k in symbol natural code string
        do
            python generate_question.py --max_obj $i --fact_cnt $j --context_type $k --task_type ind_deductive
            # python generate_question.py --max_obj $i --fact_cnt $j --context_type $k --task_type deductive
        done   
    done
done