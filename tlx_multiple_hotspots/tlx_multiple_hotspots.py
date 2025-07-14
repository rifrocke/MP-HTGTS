# This script is to analyse the junction numbers of multiple specified hotspots.
# Writer: Dr Jinglong Wang

import pandas as pd
import numpy as np
import os
import argparse

# --- Argument Parsing ---
parser = argparse.ArgumentParser(description='To obtain the number of junctions in specified hotspots (hs), such as bait and prey')

parser.add_argument("-i", dest="input_folder", type=str, required=True,
                    help="Input folder containing .tlx files")

parser.add_argument("-m", dest="metadata", type=str, required=True,
                    help="Metadata file containing hotspots (format: name, chr, hotspot start(include) and hotspot end(open))")

parser.add_argument("-o", dest="output_folder", type=str, default="stats_of_hotspots",
                    help="Output stats folder (Default: 'stats_of_hotspots' in current location)")
args = parser.parse_args()

# --- Setup Directories ---
output_path = os.path.join(os.getcwd(), args.output_folder)
os.makedirs(output_path, exist_ok=True)
print(f"Output directory set to: {output_path}")

# Read the metadata file.
meta = pd.read_csv(args.metadata, sep="\t", header=None, names=['name', 'chr', 'hotspot_start', 'hotspot_end'])
meta['hotspot_start'] = pd.to_numeric(meta['hotspot_start'], errors='coerce').astype('Int64') 
meta['hotspot_end'] = pd.to_numeric(meta['hotspot_end'], errors='coerce').astype('Int64') 

# Drop rows from metadata if hotspot coordinates couldn't be converted (i.e., are NaN).
meta.dropna(subset=['hotspot_start', 'hotspot_end'], inplace=True)
if meta.empty:
    print("❌ Error: No valid hotspot ranges found in metadata after conversion. Please check your metadata file format.")
    exit() 

print(f"Metadata loaded from: {args.metadata}")

# Get list of files from the specified input folder.
file_list = os.listdir(args.input_folder)

# Filter for files ending with '.tlx'.
file_list_tlx = [file for file in file_list if file.endswith('.tlx')]

# Initialize an empty DataFrame to store all results.
stats = pd.DataFrame([])

# --- Process .tlx Files ---
if not file_list_tlx:
    print(f"⚠️ No .tlx files found in the input folder: {args.input_folder}. Exiting.")
else:
    print(f"Found {len(file_list_tlx)} .tlx files to process.")
    for fl in file_list_tlx:
        file_path = os.path.join(args.input_folder, fl)
        file_name = os.path.splitext(fl)[0]

        try:
            df_genome = pd.read_csv(file_path, sep='\t', low_memory=False)
            # Explicitly convert 'Junction' column to numeric.
            # `errors='coerce'` will turn non-numeric values into NaN.
            df_genome['Junction'] = pd.to_numeric(df_genome['Junction'], errors='coerce')
            # Drop rows where 'Junction' could not be converted (are NaN).
            df_genome.dropna(subset=['Junction'], inplace=True)
            # Convert to integer type after dropping NaNs for comparison.
            df_genome['Junction'] = df_genome['Junction'].astype(np.int64)

            print(f"Processing file: {fl} (Total junctions after cleaning: {len(df_genome)})")
        except Exception as e:
            print(f"❌ Error reading or cleaning file {fl}: {e}. Skipping this file.")
            continue

        # If the dataframe is empty after cleaning, skip.
        if df_genome.empty:
            print(f"  Skipping {fl} as it contains no valid junction data after cleaning.")
            continue

        total_junction = len(df_genome)
        current_file_stats = {"file_name": file_name, "total_junctions": total_junction}

        df_genome_neg = df_genome.loc[df_genome['Strand'] == -1]
        df_genome_pos = df_genome.loc[df_genome['Strand'] == 1]

        for j in range(len(meta)):
            hotspot_name = meta.iloc[j]['name']
            hotspot_chr = meta.iloc[j]['chr']
            hotspot_start = meta.iloc[j]['hotspot_start']
            hotspot_end = meta.iloc[j]['hotspot_end']

            # Ensure hotspot coordinates are not NaN from metadata conversion
            if pd.isna(hotspot_start) or pd.isna(hotspot_end):
                print(f"  Skipping hotspot '{hotspot_name}' due to invalid coordinates in metadata.")
                continue

            df_hs_neg = df_genome_neg.loc[df_genome_neg['Rname'] == hotspot_chr]
            df_hs_pos = df_genome_pos.loc[df_genome_pos['Rname'] == hotspot_chr]

            # Calculate the number of junctions within the hotspot's genomic region.
            hs_neg = len(df_hs_neg.loc[(df_hs_neg['Junction'] >= hotspot_start) & (df_hs_neg['Junction'] < hotspot_end)])
            hs_pos = len(df_hs_pos.loc[(df_hs_pos['Junction'] >= hotspot_start) & (df_hs_pos['Junction'] < hotspot_end)])
            hs_total = hs_neg + hs_pos

            current_file_stats[f"{hotspot_name}_both"] = hs_total
            current_file_stats[f"{hotspot_name}_neg"] = hs_neg
            current_file_stats[f"{hotspot_name}_pos"] = hs_pos

        stats = pd.concat([stats, pd.DataFrame([current_file_stats])], ignore_index=True)

# --- Save Results ---
if not stats.empty:
    output_file_path = os.path.join(output_path, 'stats_of_hotspots.csv')
    stats.to_csv(output_file_path, index=False)
    print(f"\n✅ All processing complete! Results saved to: {output_file_path}")
else:
    print("\nℹ️ No statistics were generated. Please check your input files and metadata.")
