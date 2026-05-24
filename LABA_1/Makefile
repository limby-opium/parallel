CXX      = g++
CXXFLAGS = -O2 -fopenmp -std=c++17 -Iinclude
SRC      = src/main.cpp
OUT      = main

all: $(OUT)

$(OUT): $(SRC) include/matrix_utils.h
	$(CXX) $(CXXFLAGS) -o $(OUT) $(SRC)

run: $(OUT)
	./$(OUT)

benchmark: $(OUT)
	bash benchmark.sh

verify:
	python3 verify.py result/A.txt result/B.txt result/result.txt

plot:
	python3 plot.py

clean:
	rm -f $(OUT) result/*

.PHONY: all run benchmark verify plot clean