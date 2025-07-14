# This scripts is to filtered the library cross-contamintion in tlx files based on the second barcode MID2.
# Writer: Dr Jinglong Wang 

import pandas as pd
import numpy as np
import os
import argparse

def RCP(sequence):
  Complement={'A':'T','T':'A','G':'C','C':'G'}
  return "".join(Complement.get(base,base) for base in reversed(sequence))


parser = argparse.ArgumentParser(description='Filter out the contamination reads based on the MID2 in input folder to generate clean files in target folder')
parser.add_argument("-i", dest = "input_folder", type = str, required = True,
                              help = "Input folder" )
parser.add_argument("-m", dest = "metadata", type = str, required = True,
                              help = "metadata file.txt" )
parser.add_argument("-o", dest = "output_folder", type = str, default = "MID2_filtered",
                              help = "Output filtered folder (Default: 'MID2_filtered' in current location)" )
args = parser.parse_args()

metafolder= args.input_folder
filelist=os.listdir(metafolder)
meta=pd.read_csv(args.metadata, sep="\t")
tlxList = meta["Library"]
os.chdir(metafolder)
os.mkdir(args.output_folder)

stats = pd.DataFrame([])
for i in range(len(tlxList)):
  libName = tlxList[i]
  fileName = [j for j in filelist if str(libName) in j ] 
  df_genome=pd.read_csv(fileName[0],sep='\t', low_memory=False)
  preCleanRead = len(df_genome)
  ref_MID2 = RCP(meta["MID2"][i])
  Barcode2=df_genome['Seq'].squeeze().str.slice(start=-5)
  df_genome['Barcode2']=Barcode2
  df_genome.drop(df_genome[df_genome['Barcode2'] != ref_MID2].index, inplace=True)
  postCleanRead = len(df_genome)
  output_file= fileName[0]
  output_location = os.path.join(args.output_folder, output_file)
  df_genome.to_csv(output_location, sep='\t', index= False)

  a = pd.DataFrame({"fileName":fileName,"PreCleanRead":preCleanRead,"PostCleanRead":postCleanRead})

  stats1= pd.concat([stats, a],ignore_index=True)

stats_file= stats1.to_csv(os.path.join(args.output_folder, 'stats.csv'),index=False)


