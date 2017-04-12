#!/bin/bash

FILES=$(exec find -name '*.png')
for f in $FILES
do
#  echo $f
  identify $f
  convert $f -strip $f
  identify $f
done
