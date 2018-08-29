#!/bin/bash

PORT="$UID"

echo -e "Spinning up your Jupyter Notebook! (Give me about 5s...)"
batch="$(sbatch --parsable jupyter-notebooks.slurm $PORT)"
sleep 5
echo -e "\nJobID: $batch"

host="$(squeue -j $batch -o %N | grep evc)"

echo -e "\nNow that it's running, you need to run (open a new terminal and paste this):"
echo -e "\n    ssh -NL 19972:$host:$PORT $USER@newton.ist.ucf.edu"
echo -e "\nOnce you've run the above command, open a browser and head to http://localhost:19972/"