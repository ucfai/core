#!/bin/bash
#SBATCH --job-name=%u
#SBATCH --output=sigai-%j.log
#SBATCH --ntasks=1
#SBATCH --mem=8gb
#SBATCH --time=02:00:00

date;hostname;pwd

export XDG_RUNTIME_DIR=$HOME/tmp

source activate sigai-fa18

jupyter notebook --no-browser --port=$1 --ip='*' --NotebookApp.token=''

date
