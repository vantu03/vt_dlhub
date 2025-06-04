import requests, re, os, json, mimetypes
from bs4 import BeautifulSoup

class DLHub:
    
    def __init__(
        self,
        url,
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Mobile/15E148 Safari/604.1',
            'Accept-Language': 'en-US,en;q=0.9',
        },
        output_prefix="dlhub_",
        output_dir=None,
        filename=None
    ):
        self.input_url = url
        self.output_prefix = output_prefix
        self.output_dir = output_dir
        self.filename = filename
        self.headers = headers
        self.result = {"media": [], "trys": 0}
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
            resp.raise_for_status()
            if self.output_dir:
                os.makedirs(self.output_dir, exist_ok=True)
                file_path = os.path.join(self.output_dir, media['filename'])
            else:
                file_path = media['filename']

            with open(file_path, "wb") as f:
                f.write(resp.content)

            return file_path

        except Exception as e:
            print(str(e))
            
    def run(self, download=False, maxtrys=3):
        
        while self.result['trys'] < maxtrys:

            self.result['trys'] += 1

            try:

                resp = requests.get(self.input_url, headers=self.headers, allow_redirects=True, timeout=10)
                resp.raise_for_status()

                self.result["final_url"] = resp.url
                
                match = re.search(r'/(video|photo)/(\d+)', self.result["final_url"])
                
                media_type = match.group(1)
                media_id = match.group(2)
                
                soup = BeautifulSoup(resp.text, "html.parser")
                script_tag = soup.find("script", {"id": "__UNIVERSAL_DATA_FOR_REHYDRATION__"})
                
                if script_tag:
                    data = json.loads(script_tag.string)

                    scopes = ["webapp.video-detail", "webapp.reflow.video.detail"]
                    
                    for scope in scopes:

                        #Meta
                        meta = (
                            data.get("__DEFAULT_SCOPE__", {})
                                .get(scope, {})
                                .get("shareMeta", {})
                        )
                        if meta:
                            self.result['title'] = meta.get('title', '')
                            self.result['desc'] = meta.get('desc', '')
                            self.result['cover_url'] = meta.get('cover_url', '')

                        #Video
                        video = (
                            data.get("__DEFAULT_SCOPE__", {})
                                .get(scope, {})
                                .get("itemInfo", {})
                                .get("itemStruct", {})
                                .get("video", {})
                        )

                        if video:
                            if video.get('playAddr'):
                                self.result['media'].append({
                                    'type': 'video',
                                    'url': video.get('playAddr'),
                                    'cookies': resp.cookies.get_dict(),
                                    'id': media_id,
                                    'width': video.get('width', None),
                                    'height': video.get('height', None),
                                    'filename': self.getFileName(media_id, 'mp4'),
                                })
                                
                            if video.get('cover'):
                                self.result['cover'] = video.get('cover', '')
                        #Music
                        music = (
                            data.get("__DEFAULT_SCOPE__", {})
                                .get(scope, {})
                                .get("itemInfo", {})
                                .get("itemStruct", {})
                                .get("music", {})
                        )

                        if music and music.get('playUrl'):
                            self.result['media'].append({
                                'type': 'music',
                                'url': music.get('playUrl'),
                                'cookies': resp.cookies.get_dict(),
                                'id': media_id,
                                'width': None,
                                'height': None,
                                'filename': self.getFileName(media_id, 'mp3'),
                            })
                            
                        #URL Images
                        images = (
                            data.get("__DEFAULT_SCOPE__", {})
                                .get(scope, {})
                                .get("itemInfo", {})
                                .get("itemStruct", {})
                                .get("imagePost", {})
                                .get("images", [])
                        )
                        
                        if images:

                            for image in images:
                                for imageURL in image.get('imageURL', []).get('urlList', []):
                                    self.result['media'].append({
                                        'type': 'image',
                                        'url': imageURL,
                                        'cookies': resp.cookies.get_dict(),
                                        'id': media_id,
                                        'width': image.get('imageWidth', None),
                                        'height': image.get('imageHeight', None),
                                        'filename': self.getFileName(media_id, 'jpg'),
                                    })
                
                    if download:
                        
                        for index, item in enumerate(self.result["media"]):
                            path = self.download_file(item)
                            if path:
                                item['path'] = path 
                        

                    self.result["success"] = True
                    if self.result['media']:
                        break

            except Exception as e:
                self.result["error"] = self.result.get("error", "") + "\n[Try {}] {}".format(self.result["trys"], str(e))
                if self.result['trys'] == maxtrys:
                    self.result["success"] = False
                else:
                    time.sleep(1)

        return self.result