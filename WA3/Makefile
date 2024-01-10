################################################################################
# Makefile for general code snippets
#
# by André Pereira
################################################################################

SHELL = /bin/sh
BIN_NAME = MDpar.exe

CXX = nvcc
LD  = nvcc

#CXXFLAGS   = -O2 -g -std=c++11 -arch=sm_35 -Wno-deprecated-gpu-targets 
CXXFLAGS   = -O2 -g -std=c++11 -Wno-deprecated-gpu-targets 

CC = gcc
CFLAGS = -O3 -pg -ftree-vectorize -msse4 -g -fno-omit-frame-pointer -funroll-loops -finline-functions # select optimization flags (e.g., O2 or O3)


SRC_DIR = src
BIN_DIR = bin
BUILD_DIR = build
SRC = $(wildcard $(SRC_DIR)/*.cu)
OBJ = $(patsubst src/%.cu,build/%.o,$(SRC))
BIN = $(BIN_NAME)

BIN_SEQ_NAME = MDseq.exe
SRC_SEQ = $(SRC_DIR)/MDseq.cpp

LOAD_GCC = module load gcc/9.3.0
LOAD_CUDA = module load cuda/11.3.1

vpath %.cu $(SRC_DIR)

################################################################################
# Rules
################################################################################

.DEFAULT_GOAL = all

$(BUILD_DIR)/%.o: %.cu
	@mkdir -p $(BUILD_DIR)
	$(LOAD_GCC); \
	$(LOAD_CUDA); \
	$(CXX) -c $(CXXFLAGS) $(INCLUDES) $< -o $@ $(LIBS)

$(BIN_DIR)/$(BIN_NAME): $(OBJ)
	@mkdir -p $(BIN_DIR)
	$(LOAD_GCC); \
	$(LOAD_CUDA); \
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $(OBJ) $(LIBS)


$(BIN_DIR)/$(BIN_SEQ_NAME): $(SRC_SEQ)
	@mkdir -p $(BIN_DIR)
	$(LOAD_GCC); \
	$(LOAD_CUDA); \
	$(CC) $(CFLAGS) $(SRC_SEQ) -lm -o $(BIN_DIR)/$(BIN_SEQ_NAME)

all: $(BIN_DIR)/$(BIN_NAME) $(BIN_DIR)/$(BIN_SEQ_NAME)


clean:
	rm -f $(BUILD_DIR)/* $(BIN_DIR)/*

run:
	$(LOAD_GCC); \
	$(LOAD_CUDA); \
	sbatch run.sh

runhost:
	$(LOAD_GCC); \
	$(LOAD_CUDA); \
	bash run.sh

runseq:
	$(LOAD_GCC); \
	$(LOAD_CUDA); \
	$(BIN_DIR)/$(BIN_SEQ_NAME) < inputdata.txt

