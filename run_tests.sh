#!/bin/bash
root = pwd
for f in $(find . -name 'test');
do
    cd $f;
    python -m unittest discover --pattern=*Test.py
    cd $root;
done
