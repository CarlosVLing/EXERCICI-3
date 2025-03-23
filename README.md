# Exercise 3: Catalan Whisper for Valencian Texts

This repository is part of a Master's Thesis whose goal is evaluating and improvinf the performance of Whisper in the transcription of Valencian Catalan.

## 📌 **Description of the project**

This project is the starting point for a master's thesis focused on evaluating and improving Whisper's performance for Valencian Catalan texts. Specifically, it analyzes the model's errors and it was also a goal to propose a fine-tuning approach to improve its performance in this language variety (not yet done, in development during the moment).

## 📂 **Repository Structure**
- `scripts/` → Python scripts for data processing and format conversion
- `finetining_dataset/` → Resources for future fine-tuning (the file `CAMPANAR_NET.vtt` is the clean version of the downloaded subtitles of the episode used for fine-tuning).
- `Resum d'errors.xlsx` → the excel file with the summary of annotated errors by the moment
- `SUBS_FOR_LABELLING.csv` → the dataset used for annotation

## 🛠 **Materials and Methods**

### 🔹 **Used Modeñ**
Used **Whisper-large-v3** thanks to **CLiC and STeL at UB**.

### 🔹 **Corpus Analysis**
- An episode of **Zoom** from **À Punt** public broadcaster was used.
- Reasons: the topic treated in the program and its format, a documentary, formal and produced, that ensures a reliability on the subtitles provided.
- Subtitles downloaded with **yt-dlp**.

### 🔹 **Used tools**
- Subtitles downloaded with **yt-dlp**.
- **Label Studio**: Fon annotation of errors, in a coda environment, the html template can be found in this repository.
- **Python scripts provided in the scripts folder**

## 📊 **Errors analysis so far (Annotation still under development)**

### 🔸 **Main detected errors**
**115 errors detected in 30 minutes of audio**, exempt bits not included in the error count but counted in the time count. Most frequent ones were:

1. **Wrong language identification** (45 cases):
   - Example: *"En los años sesenta, existía una preocupación"* instead of *"En els anys seixanta existia una preocupació"*.
   - The model tends to identify Valencian Catalan bits after spanish bits as if they were Spanish, despite there being linguistic cues of code-switch.

2. **Dialectological Inadaptations** (26 casos):
   - Model substitutes genuine Vlencian terms for central catalan terms.
   - Example: *"este" → "aquest"*, *"ahui" → "avui"*.
   - Problems identifying genuine valencian linguistic cues: *"s’assenta" → "se senta"*. (omission of unstressed /a/ as a phoneme)

3. **Other linguistic errors**:
   - Omissions.
   - Hallucinations.
   - Problems with question intonation.

## 🎯 *Next Steps**

Although fine-tuning was not completed within the project timeframe, the following were achieved:
- Creating a fine-tuning database with another Zoom episode with contexts similar to those where the model failed.
- Establishing an error classification for future improvements.

Specific training with corpora in Valencian varieties is expected to improve the detection and transcription of the Whisper model in these cases.
  

