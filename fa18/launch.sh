#!/bin/bash

PORT="$UID"

batch="$(sbatch --parsable jupyter-notebooks.slurm $PORT)"
echo "$batch"

echo "$MY_HOST"

echo "\nSpinning up your Jupyter Notebook!"
echo "\nNow that it's running, you need to run:"
echo "\n    ssh -NL $PORT:$MY_HOST:19972 $USER@newton.ist.ucf.edu"
echo "Once you've run ^, open a browser and head to http://localhost:19972/"