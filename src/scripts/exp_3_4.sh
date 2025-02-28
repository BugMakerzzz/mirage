#!/bin/bash
for i in symbol natural code 
do
    for j in symbol natural code 
    do
        if [ $i = $j ]
        then
            echo ok
        else
            python inference.py --context_type $j --task_type deductive --model $1 --target_type $i --method $2
        fi
    done 
done