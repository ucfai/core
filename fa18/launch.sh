#!/bin/bash

PORT="$UID"

batch="$(sbatch --parsable jupyter-notebooks.slurm $PORT)"
echo "$batch"

host=$(squeue -j $batch -o %N | grep "evc")

echo -e "Spinning up your Jupyter Notebook!"
echo -e "Now that it's running, you need to run:"
echo -e "    ssh -NL $PORT:$host:19972 $USER@newton.ist.ucf.edu"
echo -e "Once you've run ^, open a browser and head to http://localhost:19972/"