import os
import re
import sys
import subprocess
import argparse
import tempfile

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

def download_captions(url, lang="en", shorten=False, output_dir="."):
    """Download and clean YouTube captions using a temporary directory."""
    # Check if yt-dlp is installed
    try:
        subprocess.run(["yt-dlp", "--version"], check=True, stdout=subprocess.DEVNULL)
    except FileNotFoundError:
        print("Error: yt-dlp is not installed. Please install it using `pip install yt-dlp`.")
        sys.exit(1)

    # Use a temporary directory within the output_dir.
    with tempfile.TemporaryDirectory(dir=output_dir) as temp_dir:
        # Save current directory and change to temp_dir
        current_dir = os.getcwd()
        os.chdir(temp_dir)

        # Set output options if using short file names
        output_opts = ["-o", "%(id)s.%(ext)s"] if shorten else []

        # Download subtitles
        subprocess.run([
            "yt-dlp", "--write-auto-sub", "--sub-lang", lang, "--skip-download"
        ] + output_opts + [url], check=True)

        # Return to the original directory
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

    print(f"Captions have been saved to {output_dir}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Caption Downloader")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("--lang", default="en", help="Caption language (default: en)")
    parser.add_argument("--shorten", action="store_true", help="Use short file names")
    parser.add_argument("--output", default=".", help="Output directory (default: current directory)")
    args = parser.parse_args()

    download_captions(args.url, args.lang, args.shorten, args.output)
