# This script is to count the reads with unique Qname in tlx files.

# Writer: Dr Jinglong Wang

import pandas as pd
import numpy as np
import os
import argparse

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description='To obtain the number of total reads and unique reads from .tlx files.')

parser.add_argument("-i", dest="input_folder", type=str, required=True,
                    help="Input folder containing .tlx files.")

parser.add_argument("-o", dest="output_folder", type=str, default="stats_of_counts",
                    help="Output stats folder (Default: 'stats_of_counts' in current location).")
args = parser.parse_args()

# --- Setup Directories ---
output_path = os.path.join(os.getcwd(), args.output_folder)

# Create the output directory.
os.makedirs(output_path, exist_ok=True)
print(f"Output directory set to: {output_path}")

file_list = os.listdir(args.input_folder)

stats = pd.DataFrame([])

# --- File Filtering ---
file_list_tlx = [file for file in file_list if file.endswith('.tlx')]

# --- Process .tlx Files ---
if not file_list_tlx:
    print(f"⚠️ No .tlx files found in the input folder: {args.input_folder}. Exiting.")
else:
    print(f"Found {len(file_list_tlx)} .tlx files to process.")

    for i, fl in enumerate(file_list_tlx): 
        file_path = os.path.join(args.input_folder, fl)
        file_name = os.path.splitext(fl)[0] 

        try:
            df = pd.read_csv(file_path, sep='\t', low_memory=False)
            print(f"Processing file: {fl}")
        except Exception as e:
            print(f"❌ Error reading file {fl}: {e}. Skipping this file.")
            continue # Skip to the next file if there's an error.

        df_relevant_columns = df[['Qname', 'JuncID']]

        # To count the total junctions (some reads have >1 junction).
        total_wrong_reads = len(df_relevant_columns)

        # Count unique reads where 'JuncID' is 1.
        df_unique = df_relevant_columns.loc[df_relevant_columns['JuncID'] == 1]
        total_unique_reads = len(df_unique)

        # Create a dictionary for the current file's statistics.
        current_file_stats = {
            "file_name": file_name,
            "total_wrong_reads": total_wrong_reads,
            "total_unique_reads": total_unique_reads
        }
        stats = pd.concat([stats, pd.DataFrame([current_file_stats])], ignore_index=True)

# --- Save Results ---
if not stats.empty:
    output_file_path = os.path.join(output_path, 'stats_of_total_unique_reads.csv')
    stats.to_csv(output_file_path, index=False)
    print(f"\n✅ All processing complete! Results saved to: {output_file_path}")
else:
    print("\nℹ️ No statistics were generated. Please check your input files and ensure they are valid .tlx files.")