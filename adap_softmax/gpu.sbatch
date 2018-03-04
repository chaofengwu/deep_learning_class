#!/bin/bash
#SBATCH --output=/home/chaofeng/slurm/slurm_out/%j.%N.stdout
#SBATCH --error=/home/chaofeng/slurm/slurm_out/%j.%N.stderr
#SBATCH --partition=pascal
#SBATCH --job-name=get_tesla_info

export PATH=$PATH:/usr/local/cuda/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH=/usr/local/cuda/lib64
source /etc/profile.d/modules.sh



cd /scratch/chaofeng/TTIC31230/LSTM
bash test.sh