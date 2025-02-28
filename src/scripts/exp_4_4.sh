#!/bin/bash
for i in 0 1 2 3
do 
    for j in 1
    do
        # python make_neighbor.py --nb_level $j --nb_type if --max_obj 5 --cls $i
        # python make_neighbor.py --nb_level $j --nb_type cf --max_obj 5 --cls $i
        # python make_neighbor.py --nb_level $j --nb_type of --max_obj 5 --cls $i
        # python make_neighbor.py --max_obj 5 --cls $i
        # python generate_question.py --max_obj 5 --cls $i --test_cnt 5
        # python generate_question.py --nb_type if --nb_level $j --max_obj 5 --cls $i --test_cnt 5
        # python generate_question.py --nb_type cf --nb_level $j --max_obj 5 --cls $i --test_cnt 5
        # python generate_question.py --nb_type of --nb_level $j --max_obj 5 --cls $i --test_cnt 5
        python multi_inference.py --model $1 --max_obj 5 --method $2 --cls $i
        python multi_inference.py --nb_type if --nb_level 1 --model $1 --max_obj 5 --method $2 --cls $i
        python multi_inference.py --nb_type cf --nb_level 1 --model $1 --max_obj 5 --method $2 --cls $i
        python multi_inference.py --nb_type of --nb_level 1 --model $1 --max_obj 5 --method $2 --cls $i
    done
done
for i in 0
do 
    for j in 2 3
    do
        # python make_neighbor.py --nb_level $j --nb_type if --max_obj 5 --cls $i
        # python make_neighbor.py --nb_level $j --nb_type cf --max_obj 5 --cls $i
        # python make_neighbor.py --nb_level $j --nb_type of --max_obj 5 --cls $i
        # python make_neighbor.py --max_obj 5 --cls $i
        # python generate_question.py --max_obj 5 --cls $i --test_cnt 5
        # python generate_question.py --nb_type if --nb_level $j --max_obj 5 --cls $i --test_cnt 5
        # python generate_question.py --nb_type cf --nb_level $j --max_obj 5 --cls $i --test_cnt 5
        # python generate_question.py --nb_type of --nb_level $j --max_obj 5 --cls $i --test_cnt 5
        python multi_inference.py --model $1 --max_obj 5 --method $2 --cls $i
        python multi_inference.py --nb_type if --nb_level $j --model $1 --max_obj 5 --method $2 --cls 0
        python multi_inference.py --nb_type cf --nb_level $j --model $1 --max_obj 5 --method $2 --cls 0
        python multi_inference.py --nb_type of --nb_level $j --model $1 --max_obj 5 --method $2 --cls 0
    done
done