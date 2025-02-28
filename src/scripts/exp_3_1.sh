#!/bin/bash
for task in inductive deductive
do  
    for model in qwq marco_o1
    do
        # python inference.py --task_type $task --model $model --datalength 100 --method direct_5
    
        python inference.py --max_obj $i --fact_cnt $j --context_type symbol --task_type deductive --model $1 --datalength 500 --method $2
        python inference.py --max_obj $i --fact_cnt $j --context_type natural --task_type inductive --model $1 --datalength 500 --method $2
        python inference.py --max_obj $i --fact_cnt $j --context_type natural --task_type deductive --model $1 --datalength 500 --method $2
        python inference.py --max_obj $i --fact_cnt $j --context_type code --task_type inductive --model $model --datalength 500
        python inference.py --max_obj $i --fact_cnt $j --context_type code --task_type deductive --model $1 --datalength 500 --method $2
        python inference.py --max_obj $i --fact_cnt $j --context_type string --task_type inductive --model $1 --datalength 500 --method $2
        python inference.py --max_obj $i --fact_cnt $j --context_type string --task_type deductive --model $1 --datalength 500 --method $2
    done
done