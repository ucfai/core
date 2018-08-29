#!/bin/bash

PORT="$UID"

echo -e "Spinning up your Jupyter Notebook! (Give me about 5s...)"
batch="$(sbatch --parsable jupyter-notebooks.slurm $PORT)"
sleep 5
echo "\nJobID: $batch"

host="$(squeue -j $batch -o %N | grep evc)"

echo -e "\nNow that it's running, you need to run (in a new terminal window):"
echo -e "\n    ssh -NL 19972:$host:$PORT $USER@newton.ist.ucf.edu"
echo -e "\nOnce you've run ^, open a browser and head to http://localhost:19972/"