#!/bin/bash

PORT="$UID"

batch="$(sbatch --parsable jupyter-notebooks.slurm $PORT)"
echo -e "$batch"

echo -e "\nSpinning up your Jupyter Notebook!"
echo -e "\nNow that it's running, you need to run:"
echo -e "\n    ssh -NL $PORT:$(hostname):19972 $USER@newton.ist.ucf.edu"
echo -e "\nOnce you've run ^, open a browser and head to http://localhost:19972/"