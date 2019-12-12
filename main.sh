#!/bin/bash

python3 main.py $1
llc -filetype=obj output.ll
gcc output.o -o output -static
./output
