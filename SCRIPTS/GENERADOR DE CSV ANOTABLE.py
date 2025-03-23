#GENERADOR DE CSV ANOTABLE

import pandas as pd

# Load CSV files
subs_orig = pd.read_csv('SUBS_ORIG.csv')
subs_auto = pd.read_csv('SUBS_AUTO.csv')

# Put files together
merged = pd.merge(subs_orig, subs_auto, on='Interval Start (s)', suffixes=('_original', '_auto'))

# Rename the columns for the annotation template
merged.rename(columns={
    'Subtitles_original': 'original_subtitles',
    'Subtitles_auto': 'automatic_subtitles'
}, inplace=True)

# Save file
output_path = 'merged_annotations.csv'
merged.to_csv(output_path, index=False)