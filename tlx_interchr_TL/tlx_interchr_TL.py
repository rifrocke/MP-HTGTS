# This script is to count the junctions in inter-chromosomes.
# Writer: Dr Jinglong Wang

import pandas as pd
import numpy as np
import os
import argparse

parser = argparse.ArgumentParser(description='To obtain the number of junctions in specified hotspots (hs), such as bait and prey')

parser.add_argument("-i", dest = "input_folder", type = str, required = True,
                              help = "Input folder" )

parser.add_argument("-c", dest = "chr_bait", type = str, required = True,
                              help = "The chromosome of bait, chrN" )

parser.add_argument("-o", dest = "output_folder", type = str, default = "interchr_TL",
                              help = "Output stats folder (Default: 'interchr_TL' in current location)" )
args = parser.parse_args()

file_list=os.listdir(args.input_folder)
os.chdir(args.input_folder)
os.makedirs(args.output_folder, exist_ok=True) 

stats = pd.DataFrame([]) # Initialize an empty DataFrame

ch_bait = args.chr_bait

# Sanity check -optional if all the files are bed files in the input folder.
file_list_tlx = [file for file in file_list if file.endswith('.tlx')] 

for i in range(len(file_list_tlx)):
  fl = file_list_tlx[i]
  file_name = fl.replace(".tlx", "")
  df_genome = pd.read_csv(fl, sep='\t', low_memory=False)

  # To count the total junctions
  total_junction=len(df_genome)

  # Separate negative strand and positive strand
  df_genome_neg=df_genome.loc[df_genome['Strand']==-1]
  df_genome_pos=df_genome.loc[df_genome['Strand']==1]

  # Exclude the specified chromosome of bait
  df_int_neg=df_genome_neg.loc[(df_genome_neg['Rname'] != ch_bait)]
  df_int_pos=df_genome_pos.loc[(df_genome_pos['Rname'] != ch_bait)]
  
  # calculated the number of junctions in interchromosomes
  int_neg_junction=len(df_int_neg)
  int_pos_junction=len(df_int_pos)

  # Create the row as a single-row DataFrame
  row = pd.DataFrame({"file_name":file_name,
                      "total_junctions":total_junction,
                      "int_neg_junction":int_neg_junction,
                      "int_pos_junction":int_pos_junction}, index=[0]) # Changed index=[i] to index=[0] as it's a single row DataFrame

  # Concatenate the new row (DataFrame) with the existing stats DataFrame
  stats = pd.concat([stats, row], ignore_index=True)

stats.to_csv(os.path.join(args.output_folder, 'stats_of_interchr_junctions.csv')) # Added the full filename for output csv
