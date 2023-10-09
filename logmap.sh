#!/bin/bash

#SBATCH --job-name=logmapml
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-node=1
#SBATCH --time=5-00:00:00
#SBATCH --account=drjieliu
#SBATCH --partition=drjieliu
#SBATCH --mem=300g
#SBATCH --output=pred.out
#SBATCH --mail-user=xinyubao@umich.edu
#SBATCH --mail-type=BEGIN,END
./run_total.sh