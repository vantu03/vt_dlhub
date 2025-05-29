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
dl = DLHub(url)
result = dl.run(download=True)
print(result)
```

## Output Example

For a video:

```json
{
    "media": [
        {
            "type": "video",
            "url": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o8PEYG5mI7jIoVmCtMdDfDHjNfAFPNDAqsiPEe/?a=1988&bti=ODszNWYuMDE6&ch=0&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C&cv=1&br=1064&bt=532&cs=0&ds=6&ft=-Csk_m7nPD12Nn3S9h-Ux4TFLY6e3wv25UcAp&mime_type=video_mp4&qs=0&rc=O2Y5NjM5OTZmNTdnNWk5N0Bpamc2eWs5cmk0eTMzODczNEBhNi0tYi4zNjQxNC5eY2M2YSMwZ2dyMmRzZzNgLS1kMTFzcw%3D%3D&btag=e000b8000&expire=1748716983&l=20250530024247247514848752AF8CF270&ply_type=2&policy=2&signature=7bd1833f01bd12041c04d333ea6fff43&tk=tt_chain_token",
            "cookies": {
                "ttwid": "1%7CnRNHc_nvqrHV3wp8iwdsCJyzZCPNMnjSTIKzuApOC7s%7C1748544167%7Cba034746c3b847cce0c4509bb2ead96d7b05548d681b56520ab39d93391eb7fc",
                "tt_csrf_token": "jSVLb9hI-ac-QOS2RONP2-0B2WWiaB4VSi7Q",
                "tt_chain_token": "Ef8xYmSMbTUbmdDcNDeYvA==",
                "msToken": "b7WxIVn7Nb9LSDoHLRo8qDMbFaKVUD6G3F0CqfqesWh71WzWRiL6j9RuBt2Orehmn-FJ3yZMnZA_Bn9ClZw8QyCGK4Gmj5voZBNmTg9XiYPVu9KdU-2J4O4="
            },
            "id": "7479382040887020807",
            "width": 576,
            "height": 1024,
            "filename": "dlhub_7479382040887020807.mp4",
            "path": "dlhub_7479382040887020807.mp4"
        },
        {
            "type": "music",
            "url": "https://v77.tiktokcdn.com/250894a2694f69f9bc68ba3bc0e01625/6839fc39/video/tos/maliva/tos-maliva-v-27dcd7c799-us/o8EYkAJUIDCfhIBpAmAgYuYHSBFkx8NDP1MLf4/?a=1180&bti=ODszNWYuMDE6&ch=0&cr=0&dr=0&er=0&lr=default&cd=0%7C0%7C0%7C0&br=250&bt=125&ds=5&ft=.NpOcInz7ThGijMKXq8Zmo&mime_type=audio_mpeg&qs=13&rc=anI7NnY5cjVpcjMzZzU8NEBpanI7NnY5cjVpcjMzZzU8NEBvNC8zMmRzZm5gLS1kMS9zYSNvNC8zMmRzZm5gLS1kMS9zcw%3D%3D&vvpl=1&l=20250530024247247514848752AF8CF270&btag=e00078000&cc=13",
            "cookies": {
                "ttwid": "1%7CnRNHc_nvqrHV3wp8iwdsCJyzZCPNMnjSTIKzuApOC7s%7C1748544167%7Cba034746c3b847cce0c4509bb2ead96d7b05548d681b56520ab39d93391eb7fc",
                "tt_csrf_token": "jSVLb9hI-ac-QOS2RONP2-0B2WWiaB4VSi7Q",
                "tt_chain_token": "Ef8xYmSMbTUbmdDcNDeYvA==",
                "msToken": "b7WxIVn7Nb9LSDoHLRo8qDMbFaKVUD6G3F0CqfqesWh71WzWRiL6j9RuBt2Orehmn-FJ3yZMnZA_Bn9ClZw8QyCGK4Gmj5voZBNmTg9XiYPVu9KdU-2J4O4="
            },
            "id": "7479382040887020807",
            "width": null,
            "height": null,
            "filename": "dlhub_7479382040887020807 (2).mp4",
            "path": "dlhub_7479382040887020807 (2).mp4"
        }
    ],
    "final_url": "https://www.tiktok.com/@vantumt/video/7479382040887020807",
    "title": "TikTok \u00b7 T\u00fa Mt",
    "desc": "2809 likes, 16 comments. \u201cC\u00f3 ti\u1ec1n th\u00ec ch\u00e9n ch\u00fa ch\u00e9n anh\u201d",
    "cover_url": "https://p16-sign-sg.tiktokcdn.com/tos-alisg-p-0037/oAfFGBaczCBFlUdEAInAmAAqempglng7DERMED~tplv-photomode-video-share-card:630:630:20.jpeg?lk3s=55bbe6a9&nonce=55559&refresh_token=100e13b13edac0a1a11a73b84a686660&x-expires=1780077600&x-signature=8VKGt1IDJWzxfk2LliOeO31IFZI%3D&shp=55bbe6a9&shcp=-",
    "cover": "https://p16-sign-sg.tiktokcdn.com/obj/tos-alisg-p-0037/oAfFGBaczCBFlUdEAInAmAAqempglng7DERMED?lk3s=81f88b70&x-expires=1748714400&x-signature=4dVxKlwXsNyaDl%2BO3X8rFjpF78s%3D&shp=81f88b70&shcp=-",
    "success": true
}
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.