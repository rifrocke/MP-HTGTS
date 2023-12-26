#!/usr/bin/env python3

"""
Preprocess all FASTQ files in input folder to normalized FASTQ files in target folder
"""

import sys, os
import glob
import argparse

def parse_args():
	parser = argparse.ArgumentParser(description='Preprocess all FASTQ files in input folder to normalized FASTQ files in target folder in batch mode')
	parser.add_argument("-i", dest = "preprocessfolder", type = str, required = True,
                              help = "Input Preprocess folder" )
	parser.add_argument("-n", dest = "subsample", type = int, required = True,
                              help = "Specify the number of read pairs to subsample" )
	parser.add_argument("-o", dest = "preprocessnormalizedfolder", type = str, default = "Preprocess_normalized",
                              help = "Output Preprocess_normalized folder (Default: 'Preprocess_normalized' in current location)" )
	args = parser.parse_args()
	return args

def parseFILE(args):
	# create Preprocess_normalized folder
	os.mkdir(args.preprocessnormalizedfolder)
	print("Reading FASTQ files from '%s' folder" %args.preprocessfolder)
	print("Writing Normalized FASTQ files to '%s' folder" %args.preprocessnormalizedfolder)
	
	# call seqtk on each input FASTQ file
	for file in sorted(glob.glob(args.preprocessfolder + '/*.fq.gz')):
		input_file = os.path.basename(os.path.normpath(file))
		output_file = input_file.replace(".gz", "")
		output_location =  os.path.join(args.preprocessnormalizedfolder, output_file)
		os.system('seqtk sample -s1 %s %d > %s' % (file, args.subsample, output_location))

def main():
	# check seqtk version
	print("seqtk")
	os.system('seqtk 2>&1 | grep Version')
	args = parse_args()
	parseFILE(args)

main()
