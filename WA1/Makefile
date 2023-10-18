CC = gcc
SRC = src/
CFLAGS = -O3 -pg -ftree-vectorize -msse4# none

.DEFAULT_GOAL = MD.exe

MD.exe: $(SRC)/MD.cpp
	$(CC) $(CFLAGS) $(SRC)MD.cpp -lm -o MD.exe

clean:
	rm ./MD.exe

run:
	./MD.exe < inputdata.txt
	
perf:
	srun --partition=cpar perf stat -e instructions,cycles ./MD.exe < inputdata.txt
	
perf_pessoal:
	perf stat -e instructions,cycles ./MD.exe < inputdata.txt 
