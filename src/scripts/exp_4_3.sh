#!/bin/bash

for j in 5 
do
    # python make_neighbor.py --nb_level 3 --nb_type if --fact_cnt $j --max_obj 5
    # python make_neighbor.py --nb_level 3 --nb_type cf --fact_cnt $j --max_obj 5
    # python make_neighbor.py --nb_level 3 --nb_type of --fact_cnt $j --max_obj 5
    for k in string
    do
# python filter_data.py --fact_cnt $i --fix_test
        # python generate_question.py --nb_type if --nb_level 1 --fact_cnt $j --max_obj 5 --context_type $k
        # python generate_question.py --nb_type cf --nb_level 1 --fact_cnt $j --max_obj 5 --context_type $k
        # python generate_question.py --nb_type of --nb_level 1 --fact_cnt $j --max_obj 5 --context_type $k
        # python inference.py --model $1 --fact_cnt $j --max_obj 5 --context_type $k --datalength 100 --method $2
        # python inference.py --nb_type if --nb_level 1 --model $1 --fact_cnt $j --max_obj 5 --context_type $k --datalength 100 --method $2
        python inference.py --nb_type cf --nb_level 1 --model $1 --fact_cnt $j --max_obj 5 --context_type $k --datalength 100 --method $2
        python inference.py --nb_type of --nb_level 1 --model $1 --fact_cnt $j --max_obj 5 --context_type $k --datalength 100 --method $2
    done
done 

# for k in symbol natural code string
# do
# # python filter_data.py --fact_cnt $i --fix_test
#     # python generate_question.py --nb_type if --nb_level 1 --fact_cnt $j --max_obj 5 --context_type $k
#     # python generate_question.py --nb_type cf --nb_level 1 --fact_cnt $j --max_obj 5 --context_type $k
#     # python generate_question.py --nb_type of --nb_level 1 --fact_cnt $j --max_obj 5 --context_type $k
#     # python inference.py --model $1 --fact_cnt $j --max_obj 5 --context_type $k --datalength 100 --method $2
#     python inference.py --nb_type if --nb_level 1 --model $1 --fact_cnt 5 --max_obj 5 --context_type $k --datalength 100 --method $2
#     python inference.py --nb_type cf --nb_level 1 --model $1 --fact_cnt 5 --max_obj 5 --context_type $k --datalength 100 --method $2
#     python inference.py --nb_type of --nb_level 1 --model $1 --fact_cnt 5 --max_obj 5 --context_type $k --datalength 100 --method $2
# done
