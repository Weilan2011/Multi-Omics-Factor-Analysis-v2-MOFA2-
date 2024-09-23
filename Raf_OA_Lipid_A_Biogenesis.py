import pandas as pd

# Define paths for both files
Raf_OA_HUMAnN3_Genefamilies_file = '/media/weilan/easystore/Raf-Shotgun/10_Metaphlan4_out/Raf_OA_humann_genefamilies.tsv'
Raf_OA_Lipid_A_bigenesis_genelist_file = '/media/weilan/easystore/Raf-Shotgun/Raf_LPS_protein/Raf_OA_LipidA_protein_header_HUMAnN3_matched.txt'

# Step 1: Load the first file (gene families and abundance)
df_Raf_OA_HUMAnN3_Genefamilies_file = pd.read_csv(Raf_OA_HUMAnN3_Genefamilies_file, sep='\t')

# Step 2: Read the second file (UniRef90 target genes and descriptions)
with open(Raf_OA_Lipid_A_bigenesis_genelist_file, 'r') as f:
    Raf_OA_Lipid_A_bigenesis_genelist_file_lines = f.readlines()

# Step 3: Extract the UniRef90 IDs (only the part before "|") and descriptions from the second file
Raf_OA_Lipid_A_bigenesis_genelist_file_data = {}
for line in Raf_OA_Lipid_A_bigenesis_genelist_file_lines:
    if line.startswith('UniRef90_'):
        uniref_id = line.split('|')[0]
        Raf_OA_Lipid_A_bigenesis_genelist_file_data[uniref_id] = line.strip()

# Step 4: Extract the UniRef90 IDs from the first file (gene families) and match them with the second file
matching_rows_first_file = df_Raf_OA_HUMAnN3_Genefamilies_file[
    df_Raf_OA_HUMAnN3_Genefamilies_file['# Gene Family'].apply(
        lambda x: x.split('|')[0] in Raf_OA_Lipid_A_bigenesis_genelist_file_data.keys()
    )
]

# Step 5: Add the matching descriptions from the second file
matched_descriptions = []
for uniref_id in matching_rows_first_file['# Gene Family'].apply(lambda x: x.split('|')[0]):
    matched_descriptions.append(
        Raf_OA_Lipid_A_bigenesis_genelist_file_data.get(uniref_id, "Description not found")
    )

# Step 6: Add all information from the first file and also the description from the second file
combined_df = matching_rows_first_file.copy()
combined_df['target'] = combined_df['# Gene Family'].apply(lambda x: x.split('|')[0])
combined_df['Description'] = matched_descriptions

# Step 7: Save the combined information to a new CSV file
output_combined_file_path = '/media/weilan/easystore/Raf-Shotgun/Raf_LPS_protein/LPS_combined_full_information.csv'
combined_df.to_csv(output_combined_file_path, index=False)
