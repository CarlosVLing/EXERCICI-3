##GENERADOR DE CSV SUBTÍTOLS

import csv
import re
from collections import defaultdict

#Sincronize subtitles:
def parse_vtt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    subtitle_data = []
    #Extract timestamps
    time_pattern = re.compile(r'(\d+):(\d+).(\d+) --> (\d+):(\d+).(\d+)')
    current_text = []
    current_start = None
    current_end = None
#Take 60 second fragments, taking the most recent timestamp that isn't lower than the beginning and higher than the ending of the fragment
    for line in lines:
        line = line.strip()
        match = time_pattern.match(line)
        if match:
            if current_text and current_start is not None:
                subtitle_data.append((current_start, current_end, " ".join(current_text)))
            minutes, seconds, _ = map(int, match.groups()[:3])
            end_minutes, end_seconds, _ = map(int, match.groups()[3:])
            current_start = minutes * 60 + seconds
            current_end = end_minutes * 60 + end_seconds
            current_text = []
        elif line and not line.isdigit():
            current_text.append(re.sub(r'<.*?>', '', line))

    if current_text and current_start is not None:
        subtitle_data.append((current_start, current_end, " ".join(current_text)))

    return subtitle_data

def group_subtitles(subtitle_data, interval=30):
    grouped_subtitles = defaultdict(str)
    for start_time, end_time, text in subtitle_data:
        interval_start = (start_time // interval) * interval
        interval_end = (end_time // interval) * interval

        for t in range(interval_start, interval_end + interval, interval):
            grouped_subtitles[t] += ' ' + text
    return grouped_subtitles

def save_to_csv(grouped_subtitles, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Interval Start (s)', 'Subtitles'])
        for start_time in sorted(grouped_subtitles.keys()):
            writer.writerow([start_time, grouped_subtitles[start_time].strip()])

# Usage
vtt_file_path1 = 'ZOOM-TURISME-AUTO.txt'
csv_output_path1 = 'SUBS_AUTO.csv'
subtitle_data = parse_vtt(vtt_file_path)
grouped_subtitles = group_subtitles(subtitle_data)
save_to_csv(grouped_subtitles, csv_output_path)