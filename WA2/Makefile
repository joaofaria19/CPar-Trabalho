CC = gcc
SRC = src/
CFLAGS = -O3 -pg -ftree-vectorize -msse4 -g -fno-omit-frame-pointer -funroll-loops -finline-functions # select optimization flags (e.g., O2 or O3)

.DEFAULT_GOAL = all

all: MDseq.exe MDpar.exe

MDseq.exe: $(SRC)/MDseq.cpp
	module load gcc/11.2.0; \
	$(CC) $(CFLAGS) $(SRC)MDseq.cpp -lm -o MDseq.exe

MDpar.exe: $(SRC)/MDpar.cpp
	module load gcc/11.2.0; \
	$(CC) $(CFLAGS) $(SRC)MDpar.cpp -lm -fopenmp -o MDpar.exe

clean:
	rm ./MD*.exe

runseq:
	./MDseq.exe < inputdata.txt

runpar:
	export OMP_NUM_THREADS=40; \
	./MDparN.exe < inputdata.txt

runS:
	sbatch --partition=cpar --cpus-per-task=40 time2.sh

runP:
	export OMP_NUM_THREADS=40; \
	sbatch --partition=cpar --cpus-per-task=40 time.sh


