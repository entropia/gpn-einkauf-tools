import requests

from kauf.format import msg_error
from kauf.format.log import log_debug


class HedgeDocService:
    url: str
    sid_cookie: str

    def __init__(self, url: str, sid_cookie: str = None):
        if not url.startswith("http://") or url.startswith("https://"):
            url = "https://" + url
        self.url = url
        self.sid_cookie = sid_cookie

    def new_pad(self, content: str):
        cookies = {}

        if self.sid_cookie:
            cookies['connect.sid'] = self.sid_cookie

        r = requests.post(
            self.url + "/new", data=content, headers={"Content-Type": "text/markdown"}, cookies=cookies,
        )

        log_debug(f"creating HedgeDoc pad returned status {r.status_code} and redirect to {r.url}")

        if not r.url or r.status_code >= 400 or len(r.url) < len(self.url)+4:
            msg_error("Can not create HedgeDoc pad.\nDoes the Hedge Doc require authentication? Try adding the 'connect.sid' cookie as a secret.", command_alt="kauf secrets set hedgedoc_sid XXX")

        return r.url
