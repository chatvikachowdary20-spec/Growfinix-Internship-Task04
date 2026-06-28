import os
from pathlib import Path
from openai import OpenAI

# ===============================
# SET YOUR OPENAI API KEY
# ===============================
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

# ===============================
# Read Blog/Text File
# ===============================
with open("sample_blog.txt", "r", encoding="utf-8") as file:
    text = file.read()

# ===============================
# Split Long Text into Chunks
# ===============================
MAX_CHARS = 3000

def split_text(text, max_chars):
    chunks = []
    current = ""

    sentences = text.split(". ")

    for sentence in sentences:
        if len(current) + len(sentence) < max_chars:
            current += sentence + ". "
        else:
            chunks.append(current.strip())
            current = sentence + ". "

    if current:
        chunks.append(current.strip())

    return chunks

chunks = split_text(text, MAX_CHARS)

# ===============================
# Output Folder
# ===============================
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

audio_files = []

print(f"Generating audio for {len(chunks)} chunks...")

# ===============================
# Generate Audio
# ===============================
for i, chunk in enumerate(chunks):

    speech_file = output_dir / f"part_{i+1}.mp3"

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=chunk
    )

    response.stream_to_file(speech_file)

    audio_files.append(speech_file)

    print(f"Chunk {i+1} completed.")

print("\nAudio generation finished!")

print("\nGenerated Files:")

for file in audio_files:
    print(file)
