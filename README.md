# YouTube Caption Extractor

This tool allows you to download YouTube captions (including auto-generated ones) and convert them into a readable format.

## Installation

First, install `yt-dlp`:

```sh
pip install -r requirements.txt
```

## Usage

```sh
python get_captions.py "https://www.youtube.com/watch?v=XXXXXXXXXXX" --lang en --shorten --name "custom_filename"
```

- `--lang en` : Specifies the caption language (default: en).
- `--shorten` : Uses shortened file name (video ID).
- `--name "custom_filename"` : Saves the file with the specified name (sanitized for safety). If not specified, the default name is used.

Captions are always saved in the `./output/` directory.

## License

This script is released under the MIT License.
Additionally, this tool utilizes [yt-dlp](https://github.com/yt-dlp/yt-dlp).
