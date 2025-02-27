import os
import re
import sys
import subprocess
import argparse
import tempfile
import unicodedata

def clean_captions(text):
    """Remove timestamps, HTML tags, and consecutive duplicate lines."""
    # Remove timestamps (e.g., "00:01:23.456 --> 00:01:25.789")
    text = re.sub(r'^\d{2}:\d{2}:\d{2}\.\d{3} -->.*$', '', text, flags=re.MULTILINE)

    # Remove HTML tags (e.g., "<i>text</i>" → "text")
    text = re.sub(r'<[^>]*>', '', text)

    # Remove empty lines and consecutive duplicate lines
    lines = text.split("\n")
    cleaned_lines = []
    prev_line = None
    for line in lines:
        line = line.strip()
        if line and line != prev_line:  # Remove empty & consecutive duplicate lines
            cleaned_lines.append(line)
            prev_line = line

    return "\n".join(cleaned_lines)

def sanitize_filename(name):
    """Sanitize filename to avoid unsafe characters, allowing safe Unicode characters."""
    name = unicodedata.normalize('NFKC', name)
    name = re.sub(r'[^\w\d\u4E00-\u9FFF._-]', '_', name)  # Allow alphanumeric, CJK, dot, underscore, and hyphen
    return name.strip("._-")  # Remove leading/trailing dots, underscores, or hyphens

def download_captions(url, lang="en", shorten=False, name=None):
    """Download and clean YouTube captions, save in ./output."""
    output_dir = "./output"
    os.makedirs(output_dir, exist_ok=True)

    # Check if yt-dlp is installed
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        print("Error: yt-dlp is not installed. Please install it using `pip install yt-dlp`.")
        sys.exit(1)

    # Use a temporary directory within output_dir.
    with tempfile.TemporaryDirectory(dir=output_dir) as temp_dir:
        current_dir = os.getcwd()
        os.chdir(temp_dir)

        # Set output options based on user input
        if name:
            output_opts = ["-o", f"{sanitize_filename(name)}.%(ext)s"]
        elif shorten:
            output_opts = ["-o", "%(id)s.%(ext)s"]
        else:
            output_opts = []

        # Download subtitles
        subprocess.run([
            "yt-dlp", "--write-auto-sub", "--sub-lang", lang, "--skip-download"
        ] + output_opts + [url], check=True)

        os.chdir(current_dir)

        # Process downloaded .vtt files in temp_dir
        for filename in os.listdir(temp_dir):
            if filename.endswith(".vtt"):
                input_path = os.path.join(temp_dir, filename)
                output_path = os.path.join(output_dir, filename.replace(".vtt", ".txt"))
                with open(input_path, "r", encoding="utf-8") as f:
                    raw_text = f.read()
                cleaned_text = clean_captions(raw_text)
                # Save the cleaned captions to output_path
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(cleaned_text)

    print(f"Captions have been saved to {output_path}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Caption Downloader")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--lang", default="en", help="Caption language (default: en)")
    parser.add_argument("--shorten", action="store_true", help="Use short file names")
    parser.add_argument("--name", help="Custom filename (without extension)")
    args = parser.parse_args()

    download_captions(args.url, args.lang, args.shorten, args.name)