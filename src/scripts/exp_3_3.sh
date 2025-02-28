#!/bin/bash
for i in 1 2 3 4 5 6 7 8
do
    # python filter_data.py --fact_cnt $i --fix_test
    # python generate_question.py --fact_cnt $i --task_type inductive --context_type symbol --fix_test
    # python generate_question.py --fact_cnt $i --task_type deductive --context_type symbol --fix_test
    python inference.py --fact_cnt $i --context_type symbol --task_type inductive --model $1 --fix_test --method $2
    python inference.py --fact_cnt $i --context_type symbol --task_type deductive --model $1 --fix_test --method $2
done