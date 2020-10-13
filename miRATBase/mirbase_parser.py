import os
import json

mirbase_file = "/Users/ernesto/PycharmProjects/miRATBase/static/data_store/mirbase_aliases.txt"
json_file = mirbase_file.replace(".txt",".json")

with open(mirbase_file,"r") as mf:
    lines = mf.readlines()

mb_dict = {}

for line in lines:

    val,ks = line.rstrip().split("\t")
    klist = ks.split(";")[:-1]
    for k in klist:
        mb_dict[k] = val

with open(json_file,"w") as jf:
    json.dump(mb_dict,jf)


