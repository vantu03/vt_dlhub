import requests, re, os, json, mimetypes
from bs4 import BeautifulSoup

class DLHub:
    def __init__(self, url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', 'Accept-Language': 'en-US,en;q=0.9', }, output_prefix="dlhub_", output_dir=None, filename=None):
        self.input_url = url
        self.output_prefix = output_prefix
        self.output_dir = output_dir
        self.filename = filename
        self.headers = headers
        self.result = {"media": []}
        self.count = 0
        
    def getFileCount(self, base, ext):
        
        self.count += 1
        return f"{base}.{ext}" if self.count == 1 else f"{base} ({self.count}).{ext}"

    def getFileName(self, media_id, ext):
        
        if self.filename:
            return self.getFileCount(self.filename, ext)
        else:
            return self.getFileCount(f"{self.output_prefix}{media_id}", ext)
        
    def download_file(self, media):
        
        try:
            resp = requests.get(media['url'], headers=self.headers, cookies=media['cookies'], timeout=10)

            if self.output_dir:
                os.makedirs(self.output_dir, exist_ok=True)
                file_path = os.path.join(self.output_dir, media['filename'])
            else:
                file_path = media['filename']

            with open(file_path, "wb") as f:
                f.write(resp.content)

            return file_path

        except Exception:
            return None
            
    def run(self, download=True):
        
        try:
            resp = requests.get(self.input_url, headers=self.headers, allow_redirects=True, timeout=10)
            resp.raise_for_status()
            self.result["final_url"] = resp.url
            
            match = re.search(r'/(video|photo)/(\d+)', self.result["final_url"])
            
            if match:
                media_type = match.group(1)
                media_id = match.group(2)
                
                soup = BeautifulSoup(resp.text, "html.parser")
                script_tag = soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
                
                if script_tag:
                    
                    data = json.loads(script_tag.string)
                    video_data = (
                        data.get("__DEFAULT_SCOPE__", {})
                            .get("webapp.video-detail", {})
                            .get("itemInfo", {})
                            .get("itemStruct", {})
                            .get("video", {})
                    )
                    
                    if video_data:
                        
                        play_url = video_data.get("playAddr")
                        
                        if play_url:
                
                            self.result['media'].append({
                                'type': 'video',
                                'url': play_url,
                                'cookies': resp.cookies.get_dict(),
                                'id': media_id,
                                'filename': self.getFileName(media_id, 'mp4'),
                            })
                
                resp = requests.get(f"https://www.tiktok.com/embed/v2/{media_id}", headers=self.headers, timeout=10)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")
    
                """
                if self.media_type == "video":
                    for video in soup.find_all("video", attrs={"data-testid": "play-video"}):
                        src = video.get("src")
                        if src:
                            links.append(src)
                """
                
                for img in soup.find_all("img"):
                    src = img.get("src")
                    alt = img.get("alt", "").lower()
                    cls = img.get("class", [])
        
                    if src and ("photo" in alt or "image" in alt):
                        self.result['media'].append({
                            'type': 'photo',
                            'url': src,
                            'cookies': resp.cookies.get_dict(),
                            'id': media_id,
                            'filename': self.getFileName(media_id, 'jpg'),
                        })
                
                for audio in soup.find_all("audio"):
                    self.result['media'].append({
                        'type': 'audio',
                        'url': audio.get("src"),
                        'cookies': resp.cookies.get_dict(),
                        'id': media_id,
                        'filename': self.getFileName(media_id, 'mp3'),
                    })

            
                script_tag = soup.find("script", id="__FRONTITY_CONNECT_STATE__")
                
                if script_tag:
                    
                    data = json.loads(script_tag.string)
                    
                    self.result['title'] = (
                        data.get('source', {}).
                        get('data', {}).
                        get(f'/embed/v2/{media_id}', {}).
                        get('videoData', {}).
                        get('itemInfos', {}).
                        get('text', '')
                    )
                    covers = (
                        data.get('source', {}).
                        get('data', {}).
                        get(f'/embed/v2/{media_id}', {}).
                        get('videoData', {}).
                        get('itemInfos', {}).
                        get('covers', [])
                    )
                    self.result['thumbnail'] = covers[0] if covers else ''

                    
            if download:
                for index, item in enumerate(self.result["media"]):
                    path = self.download_file(item)
                    if path:
                        item['path'] = path 
                

            self.result["success"] = True

        except Exception as e:
            self.result["success"] = False
            self.result["error"] = str(e)
    
        return self.result