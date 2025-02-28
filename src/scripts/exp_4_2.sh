#!/bin/bash
for i in 1 2 3 4
do
    # python make_neighbor.py --nb_level $i --nb_type if
    # python make_neighbor.py --nb_level $i --nb_type cf
    # python make_neighbor.py --nb_level $i --nb_type of
    # python generate_question.py --nb_type if --nb_level $i
    # python generate_question.py --nb_type cf --nb_level $i
    # python generate_question.py --nb_type of --nb_level $i
    python inference.py --nb_type if --nb_level $i --model $1 --method $2
    python inference.py --nb_type cf --nb_level $i --model $1 --method $2
    python inference.py --nb_type of --nb_level $i --model $1 --method $2
done