import requests

class HedgeDocService():
    url: str

    def __init__(self, url: str):
        if not url.startswith("http://") or url.startswith("https://"):
            url = "https://" + url
        self.url = url

    def new_pad(self, content: str):
        r = requests.post(self.url+"/new", data=content, headers={'Content-Type': 'text/markdown'})
        
        return r.url