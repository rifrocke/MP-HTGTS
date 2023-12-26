# This script is to analyse the junction numbers of multiple specified hotspots.
# Writer: Dr Jinglong Wang

import pandas as pd
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser(description='To obtain the number of junctions in specified hotspots (hs), such as bait and prey')

parser.add_argument("-i", dest = "input_folder", type = str, required = True,
                              help = "Input folder" )

parser.add_argument("-m", dest = "metadata", type = str, required = True,
                              help = "metadata file contains hotspots(format: name, chr, hotspot start(include)  and hotspot end(open))" )

parser.add_argument("-o", dest = "output_folder", type = str, default = "stats_of_hotspots",
                              help = "Output stats folder (Default: 'stats_of_hotspots' in current location)" )
args = parser.parse_args()

file_list=os.listdir(args.input_folder)
meta=pd.read_csv(args.metadata, sep="\t")
os.chdir(args.input_folder)
os.mkdir(args.output_folder)

stats = pd.DataFrame([])

# Sanity check -optional if all the files are tlx files in the input foler.
file_list_tlx = [file for file in file_list if file.endswith('.tlx')] 

for i in range(len(file_list_tlx)):
    fl=file_list_tlx[i]
    file_name =fl.replace(".tlx", "")
    df_genome=pd.read_csv(fl, sep='\t')

  # To count the total junctions
    total_junction=len(df_genome)

    dict={"file_name":file_name, "total_junctions":total_junction}

  # Separate negative strand and positive strand
    df_genome_neg=df_genome.loc[df_genome['Strand']==-1]
    df_genome_pos=df_genome.loc[df_genome['Strand']==1]

  # jump to the specified chromosome of hotspot j
    for j in range(len(meta)):
        df_hs_neg=df_genome_neg.loc[(df_genome_neg['Rname']==meta.iloc[j][1])]
        df_hs_pos=df_genome_pos.loc[(df_genome_pos['Rname']==meta.iloc[j][1])]
  
  # calculated the events of specified genomic region of hotspot j
        hs_neg=len(df_hs_neg.loc[(df_hs_neg['Junction'] >= meta.iloc[j][2]) & (df_hs_neg['Junction'] < meta.iloc[j][3])])
        hs_pos=len(df_hs_pos.loc[(df_hs_pos['Junction'] >= meta.iloc[j][2]) & (df_hs_pos['Junction'] < meta.iloc[j][3])])
        hs_total=hs_neg + hs_pos
        dict[str(meta.iloc[j][0])+"_both"]=hs_total
        dict[str(meta.iloc[j][0])+"_neg"]=hs_neg
        dict[str(meta.iloc[j][0])+"_pos"]=hs_pos
        print(dict)
  
    row = pd.DataFrame(dict,index=[i])
    stats=stats.append(row, ignore_index=True)

stats.to_csv(os.path.join(args.output_folder, 'stats_of_hotspots.csv'))

