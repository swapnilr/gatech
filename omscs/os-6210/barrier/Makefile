#OpenMP Flags Etc.
OMPFLAGS = -g -Wall -fopenmp -DLEVEL1_DCACHE_LINESIZE=`getconf LEVEL1_DCACHE_LINESIZE`
OMPLIBS = -lgomp
CC = gcc

#MPI Flags Etc (may need to customize)
MPICH = /usr/lib64/openmpi/1.4-gcc
MPIFLAGS = -g -Wall -I$(MPICH)/include
MPILIBS =
MPICC = /opt/openmpi-1.4.3-gcc44/bin/mpicc

hello_openmp: hello_openmp.c gtmp_mcs.c
	$(CC) $(OMPFLAGS) -o $@ $^ $(OMPLIBS)

hello_mpi: hello_mpi.c
	$(MPICC) $(MPIFLAGS) -o $@ $^ $(MPILIBS)

clean:
	rm -rf *.o hello_openmp hello_mpi
