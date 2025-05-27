# vt_dlhub

A lightweight and simple TikTok downloader library for Python. This package allows you to extract media (videos or photo albums) from TikTok URLs using a clean interface.

## Features

- Supports video and photo set detection
- Returns media type (`video` or `photo`)
- Fetches video title and thumbnail
- Provides fallback for non-standard TikTok URLs

## Installation

This package is not yet available on PyPI.

To install directly from GitHub:

```bash
pip install git+https://github.com/vantu03/vt_dlhub.git
````

For development (editable install):

```bash
git clone https://github.com/vantu03/vt_dlhub.git
cd vt_dlhub
pip install -e .
```

## Usage

```python
from vt_dlhub import DLHub

url = "https://www.tiktok.com/@vantumt/video/7479382040887020807"
dl = DLHub(url, download=False)
result = dl.run()

if result["success"]:
    print("Title:", result["title"])
    print("Type:", result["media_type"])
    if result["media_type"] == "video":
        print("Video URL:", result["media"][0]["url"])
    elif result["media_type"] == "photo":
        for photo in result["media"]:
            print(f"Photo {photo['index']}:", photo["url"])
```

## Output Example

For a video:

```json
{
  "success": true,
  "media_type": "video",
  "title": "Cool TikTok!",
  "thumbnail": "https://...",
  "media": [
    {"url": "https://...", "index": 1}
  ]
}
```

For a photo album:

```json
{
  "success": true,
  "media_type": "photo",
  "title": "Photo Collection",
  "thumbnail": "https://...",
  "media": [
    {"url": "https://...", "index": 1},
    {"url": "https://...", "index": 2}
  ]
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.