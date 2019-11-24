#!/bin/bash

python3 main.py
llc -filetype=obj output.ll
gcc output.o -o output -static
./output
