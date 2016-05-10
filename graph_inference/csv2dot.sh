#!/usr/bin/env bash
[[ -z $1 ]] && echo "Usage: $0 <input_name>" && exit -1;
echo "digraph G {";
cat $1 | awk -F ' ' '{print "\t", $1, "-> " $2, ";"}'
echo "}";
