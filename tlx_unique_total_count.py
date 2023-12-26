# This script is to count the reads with unique Qname in tlx files.

# Writer: Dr Jinglong Wang

import pandas as pd
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser(description='To obtain the number of total reads')

parser.add_argument("-i", dest = "input_folder", type = str, required = True,
                              help = "Input folder" )

parser.add_argument("-o", dest = "output_folder", type = str, default = "stats_of_hotspots",
                              help = "Output stats folder (Default: 'stats_of_counts' in current location)" )
args = parser.parse_args()

file_list=os.listdir(args.input_folder)
os.chdir(args.input_folder)
os.mkdir(args.output_folder)

stats = pd.DataFrame([])


# Sanity check -optional if all the files are bed files in the input foler.
file_list_tlx = [file for file in file_list if file.endswith('.tlx')] 

for i in range(len(file_list_tlx)):
  fl=file_list_tlx[i]
  file_name =fl.replace(".tlx", "")
  df=pd.read_csv(fl, sep='\t')
  df_genome=df[['Qname','JuncID']]

  # To count the total reads
  total_wrong_reads=len(df_genome)
  df_unique=df_genome.loc[df_genome['JuncID'] == 1]
  total_unique_reads=len(df_unique)

  row = pd.DataFrame({"file_name":file_name,"total_wrong_reads":total_wrong_reads, "total_unique_reads":total_unique_reads}, index=[i])

  stats=stats.append(row, ignore_index=True)

stats.to_csv(os.path.join(args.output_folder, 'stats_of_total_unique_reads.csv'))
