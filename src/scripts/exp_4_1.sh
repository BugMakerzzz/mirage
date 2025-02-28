#!/bin/bash
for nb in 1 2 4
do  
    for type in euc_of man_of min_of
    do
        python make_neighbor.py --nb_type $type --nb_level $nb
        python generate_question.py --nb_type $type --nb_level $nb
        python inference.py --nb_type $type --nb_level $nb --datalength 100 --task_type deductive --model gpt-4o
    done  
done