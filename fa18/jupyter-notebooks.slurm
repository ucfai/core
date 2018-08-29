#!/bin/bash
#SBATCH --job-name=sigai
#SBATCH --output=sigai-%j.log
#SBATCH --ntasks=1
#SBATCH --mem=8gb
#SBATCH --time=02:00:00

date;hostname;pwd
export MY_HOST="$(hostname)" 

export XDG_RUNTIME_DIR=${TMPDIR}

source activate sigai-fa18

jupyter lab --no-browser --port=$1 --ip='*' --NotebookApp.token=''

date