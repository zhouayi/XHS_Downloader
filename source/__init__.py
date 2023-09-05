from re import compile

from .Download import Download
from .Explore import Explore
from .Html import Html
from .Image import Image
from .Manage import Manager
from .Settings import Settings
from .Video import Video
import os


class XHS:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    }
    links = compile(r"https://www.xiaohongshu.com/explore/[0-9a-z]+")

    def __init__(
            self,
            path="./",
            folder="Download",
            proxies=None,
            timeout=10,
            chunk=256 * 1024,
    ):
        self.html = Html(self.headers, proxies, timeout)
        self.image = Image()
        self.video = Video()
        self.explore = Explore()
        self.download = Download(path, folder, self.headers, proxies, chunk)
        self.path = path
        self.folder = folder

    def get_image(self, container: dict, html: str, download):
        urls = self.image.get_image_link(html)
        if download:
            self.download.run(urls, container, container["作品类型"])
        container["下载地址"] = urls

    def get_video(self, container: dict, html: str, download):
        url = self.video.get_video_link(html)
        if download:
            self.download.run(url, container, container["作品类型"])
        container["下载地址"] = url

    def extract(self, url: str, download=False) -> dict:
        if not self.check(url):
            return {}
        html = self.html.get_html(url)
        if not html:
            return {}
        data = self.explore.run(html)
        path = os.path.join(self.path, self.folder, data["作品标题"] if len(data["作品标题"]) else data["作者昵称"])
        if not os.path.exists(path):
            os.mkdir(path)
        if data["作品类型"] == "视频":
            self.get_video(data, html, download)
        else:
            self.get_image(data, html, download)
        print(f"用户：{data['作者昵称']}，笔记标题：{data['作品标题']} 下载完成")
        print('--------------------------------------------------------------------------------')
        return data

    def check(self, url: str):
        return self.links.match(url)
