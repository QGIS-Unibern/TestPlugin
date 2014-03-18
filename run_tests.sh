#!/bin/bash
for f in $(find . -name 'test');
do
    cd $f;
    python -m unittest discover --pattern=*Test.py
done
