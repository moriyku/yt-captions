# YouTube Caption Extractor

This tool allows you to download YouTube captions (including auto-generated ones) and convert them into a readable format.

## Installation

First, install `yt-dlp`:

```sh
pip install -r requirements.txt
```

## Usage

```sh
python get_captions.py "https://www.youtube.com/watch?v=XXXXXXXXXXX" --lang en --shorten --output captions/
```

- `--lang en` : Specifies the caption language (default: en).
- `--shorten` : Uses shortened file name.
- `--output DIR` : Specifies the output directory (default: current directory).

## License

This script is released under the MIT License.
Additionally, this tool utilizes [yt-dlp](https://github.com/yt-dlp/yt-dlp).
