#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE}")" ; pwd -P )
cd "$parent_path"

ps aux | grep NERPY | awk '{system("kill " $2)}' #todo: properly


nohup python ./main.py nrpe.cfg //NERPY >> stdout.log 2>&1 &






