#!/usr/bin/env python3

"""
Convert all TLX files in input folder to BED/BEDGRAPH files in target folder
"""

import sys, os
import glob
import shutil
import argparse

def parse_args():
	parser = argparse.ArgumentParser(description='Convert TLX files to BED or BEDGRAPH format in batch mode')
	parser.add_argument("-i", dest = "tlxfolder", type = str, required = True,
                              help = "Input TLX folder" )
	parser.add_argument("-o", dest = "bedgraphfolder", type = str, default = "Bedgraph_files",
                              help = "Output BEDGRAPH folder (Default: 'Bedgraph_files' in current location)" )
	parser.add_argument("-g", dest = "genome", type = str, default = "human", choices={'mouse', 'human'},
                              help = "specify the genome: mouse or human (Default: human)" )
	args = parser.parse_args()
	return args

def filterfile(tlxfile):
	# convert the windows line ending to unix line ending
	os.system("perl -pi -e 's/\r\n|\n|\r/\n/g' %s" % tlxfile)
    
	# filter out undesired chromosome names
	filter_words = ['_random', '_gl']
	
	# Create a temporary output file
	temp_output_file = tlxfile + '.tmp'

	with open(tlxfile) as oldfile, open(temp_output_file, 'w') as newfile:
		for line in oldfile:
			if not any(filter_word in line for filter_word in filter_words):
				newfile.write(line)
    
	# Replace the original file with the filtered content
	try:
		os.remove(tlxfile)  # Delete the original file
		shutil.move(temp_output_file, tlxfile)  # Rename the temporary file to the original file's name
	except OSError as e:
		print(f"Error replacing file: {e}")
    
	# Return the original filename (which is now the filtered content)
	output_prefix = tlxfile.replace(".tlx", "")
	return output_prefix

def parseFILE(args):
	# create bedgraph folder
	os.mkdir(args.bedgraphfolder)
	print("Reading TLX files from '%s' folder" %args.tlxfolder)
	print("Writing BEDGRAPH files to '%s' folder" %args.bedgraphfolder)
	
	# call tlx2bed.py on each tlx file
	for file in sorted(glob.glob(args.tlxfolder + '/*.tlx')):
		output_prefix = filterfile(file)
		tlx_file = output_prefix + '.tlx'
		output_prefix_name = os.path.basename(os.path.normpath(output_prefix))
		output_location =  os.path.join(args.bedgraphfolder, output_prefix_name)
		os.system('./tlx2bed1.py -f %s -o %s -g %s --v3' % (tlx_file, output_location, args.genome))

def main():
	# check bedtools version
	os.system('bedtools --version')
	args = parse_args()
	parseFILE(args)

main()
