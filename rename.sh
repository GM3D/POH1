#!/bin/sh -xv

pattern="p_list"
subst="prices"

for file in *py *.cpp; do
    sed 's/'$pattern'/'$subst'/g' $file > $file.tmp
    mv $file.tmp $file
done