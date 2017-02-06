hpc-tools
==============================================

A set of scripts to make HPC admin life a bit easier. 
Refer to each script's help documentation for usage instructions (`commandname -h`).
All scripts are cross-platform (Windows + UNIX) unless indicated.

**diskfree** - A python equivalent of `df -h` meant to be run under Cron or Windows Task Scheduler. Emails you if disk usage passes a certain threshold. 

**sandbox** - Cap a command at a certain number of processors using CPU affinities (UNIX only). Really useful for controlling jobs/programs that otherwise attempt to detect and use every single thread on a machine.

**sge2slurm** - Converts old Sun Grid Engine (SGE) job scripts to their SLURM equivalents.

## Dependencies

These scripts have very few dependencies aside from the core Python libraries, 
but you can install them with these commands 
(aimed at RHEL-flavored distributions, but should also be pretty easy to install on Debian/Ubuntu).
You can also just install Anaconda and be done with it.

```
yum install epel-release
yum install python34 python34-devel python34-pip python34-paramiko
pip3 install psutil pandas
```
