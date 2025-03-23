import librosa
import soundfile as sf
from tqdm import tqdm

def parse_vtt(vtt_file):
    with open(vtt_file, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]

    segments = []
    i = 0

    while i < len(lines):
        # Look for timestamps
        match = re.match(r"(\d{2}):(\d{2}.\d{3}) --> (\d{2}):(\d{2}.\d{3})", lines[i])
        if match:
            start_time = (int(match.group(1)) * 60) + float(match.group(2))
            end_time = (int(match.group(3)) * 60) + float(match.group(4))

            #Capture associated transcription
            i += 1
            text_lines = []
            while i < len(lines) and not re.match(r"(\d{2}):(\d{2}.\d{3}) -->", lines[i]):
                text_lines.append(lines[i])
                i += 1

            # Join lines
            text = " ".join(text_lines).strip()
            if text:
                segments.append({
                    "audio_path": f"audio_segments/segment_{len(segments):04d}.wav",
                    "text": text,
                    "start_time": start_time,
                    "end_time": end_time
                })
        else:
            i += 1

    return segments

def extract_audio_segments(audio_file, segments, output_dir, sample_rate=16000):
    """Cut and save audio segments"""
    os.makedirs(output_dir, exist_ok=True)

    # Cargar audio completo
    audio, sr = librosa.load(audio_file, sr=sample_rate)

    dataset_entries = []

    for idx, segment in tqdm(enumerate(segments), total=len(segments), desc="Processant segments"):
        start_sample = int(segment["start_time"] * sample_rate)
        end_sample = int(segment["end_time"] * sample_rate)

        segment_audio = audio[start_sample:end_sample]
        segment_filename = f"segment_{idx:04d}.wav"
        segment_path = os.path.join(output_dir, segment_filename)

        sf.write(segment_path, segment_audio, sample_rate)

        dataset_entries.append({
            "audio_path": segment_path,
            "text": segment["text"],
            "start_time": segment["start_time"],
            "end_time": segment["end_time"]
        })

    return dataset_entries

def create_whisper_dataset(vtt_file, audio_file, output_dir, json_output):
    """Genera un dataset compatible"""
    segments = parse_vtt(vtt_file)
    dataset_entries = extract_audio_segments(audio_file, segments, output_dir)
    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(dataset_entries, f, indent=4, ensure_ascii=False)

# 🚀 Executador
vtt_file="CAMPANAR NET.vtt"
audio_file="/content/Zoom ｜ Un any de l'incendi de Campanar [1824314980757761688].mp4"
output_audio_dir="/content/segments"
json_output="dataset.json"
create_whisper_dataset(vtt_file, audio_file, output_audio_dir, json_output)
