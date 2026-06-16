# LYRA Run Guide

This guide is written for a generic LYRA user connecting for the first time and preparing the environment needed to run the Phase 3 Monte Carlo MPI case study.

## 1. Connect to LYRA

```bash
ssh corsohpcN@lglogin.hpc.unimo.it
```

Replace `corsohpcN` with your actual LYRA username.

## 2. Move to your working directory

Example:

```bash
cd /std_home/corsohpcN/group_project
```

If your files are stored somewhere else, move to that directory instead.

## 3. Load the required modules

```bash
module purge
module load slurm
module load oneapi/compiler
module load oneapi/mkl
module load oneapi/mpi
module load Anaconda3/2024.10
```

Useful checks:

```bash
which python
python --version
which mpirun
mpirun --version
which mpicc
```

At this point:

- `python` should come from `Anaconda3/2024.10`
- `mpirun` and `mpicc` should come from `oneapi/mpi`

## 4. Verify that NumPy is already available from Anaconda

```bash
python -c "import numpy; print(numpy.__version__)"
```

This is important because on LYRA it is better to reuse the NumPy installation provided by Anaconda instead of trying to build a fresh one with `pip`.

## 5. Create the virtual environment

Create it with `--system-site-packages` so that the environment can reuse the packages already provided by Anaconda, especially `numpy`.

```bash
python -m venv --system-site-packages .venv
source .venv/bin/activate
```

After activation, check again:

```bash
python -c "import numpy; print(numpy.__version__)"
```

## 6. Install `mpi4py` inside the virtual environment

Make sure the environment is active, then point the build to the MPI compiler wrapper:

```bash
export MPICC=mpicc
python -m pip install mpi4py
```

Verification:

```bash
python -c "from mpi4py import MPI; print(MPI.Get_version())"
```

Optional MPI sanity check:

```bash
mpirun -np 2 python -c "from mpi4py import MPI; comm=MPI.COMM_WORLD; print('rank', comm.Get_rank(), 'of', comm.Get_size())"
```

## 7. Prepare the project files

Make sure the working directory contains at least:

```text
mpi_montecarlo.py
```

The results file will be generated or updated by the simulation.

## 8. Prepare the Slurm job script

Example `job_montecarlo.sh`:

```bash
#!/bin/bash
#SBATCH -A dida-hpc
#SBATCH -p hpc-q
#SBATCH --time=00:10:00
#SBATCH -N 1
#SBATCH --ntasks-per-node=4
#SBATCH --mem=4g
#SBATCH --job-name=mc_mpi
#SBATCH --output=mc_mpi_%j.out
#SBATCH --error=mc_mpi_%j.err

module purge
module load slurm
module load oneapi/compiler
module load oneapi/mkl
module load oneapi/mpi
module load Anaconda3/2024.10

cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate

mpirun -np "$SLURM_NTASKS" python mpi_montecarlo.py
```

For scaling tests, change `--ntasks-per-node` to the desired number of MPI processes, for example `1`, `2`, `4`, `8`, `12`, `16`, or `20`.

## 9. Submit the job

```bash
sbatch job_montecarlo.sh
```

## 10. Monitor the queue

```bash
squeue -u corsohpcN
```

To inspect one specific job:

```bash
scontrol show job JOBID
```

## 11. Read the output and error logs

```bash
cat mc_mpi_*.out
cat mc_mpi_*.err
```

To follow the output file in real time:

```bash
tail -f mc_mpi_JOBID.out
```

## 12. Check the final results file

```bash
cat mc_results_mpi.txt
```

## 13. Download the results back to the local machine

Run this command on the local machine, not on LYRA:

```bash
scp corsohpcN@lglogin.hpc.unimo.it:/std_home/corsohpcN/group_project/mc_results_mpi.txt .
```

Adjust the remote path if your project is stored in a different directory.