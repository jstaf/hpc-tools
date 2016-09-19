hpc-tools
==============================================

A set of scripts to make HPC admin life a bit easier.

-------------------------------------------
`sandbox` - Cap a command at a certain number of processors using CPU affinities.

Usage: `sandbox [-n procs, -d, -h] -c someCommand`

+ `-c` - A bash command to be run.
+ `-n` - Cap command at <procs> number of processors. Default is 1 processor.
+ `-d` - Add a random time delay before running a job (use this if you expect to run multiple sandbox processes on the 
         same machine that will begin running more or less all at the exact same time).

-------------------------------------------
`sge2slurm` - Converts old Sun Grid Engine (SGE) job scripts to their SLURM equivalents.

Usage: `sge2slurm input_sge [output_slurm]`

+ `input_sge` - A SGE job script to be converted.
+ `output_slurm` - Filename of output SLURM script. Defaults to "`input_sge`-slurm.sh" if not set.

