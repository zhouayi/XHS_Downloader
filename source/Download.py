from pathlib import Path

from requests import exceptions
from requests import get

from PIL import Image
from tqdm import tqdm
import io


class Download:

    def __init__(
            self,
            path,
            folder,
            headers: dict,
            proxies=None,
            chunk=256 * 1024, ):
        self.root = self.init_root(path, folder)
        self.headers = headers
        self.proxies = {
            "http": proxies,
            "https": proxies,
            "ftp": proxies,
        }
        self.chunk = chunk

    @staticmethod
    def init_root(path: str, folder: str) -> Path:
        root = Path(path).joinpath(folder)
        if not root.is_dir():
            root.mkdir()
        return root

    def run(self, urls: list, data: dict, type: str):
        if type == "视频":
            path = self.root.joinpath(data["作品标题"] if len(data["作品标题"]) else data["作者昵称"], data["作品ID"] + ".mp4")
            self.download(urls[0], path, type)
        else:
            for index, url in enumerate(urls):
                name = data["作品ID"]
                path = self.root.joinpath(data["作品标题"] if len(data["作品标题"]) else data["作者昵称"], f"{name}_{index + 1}.jpg")
                self.download(url, path, type)
            

    def download(self, url: str, path, type: str):
        try:
            print(f"{type}开始下载", url)
            if type == "视频":
                with get(url, headers=self.headers, proxies=self.proxies, stream=True) as response:
                    with path.open("wb") as f:
                        for chunk in tqdm(response.iter_content(chunk_size=self.chunk)):
                            f.write(chunk)
            else:
                response = get(url, headers=self.headers, proxies=self.proxies, stream=True)
                img = Image.open(io.BytesIO(response.content))
                img = img.convert('RGB')
                img.save(path, "JPEG")
                # with get(url, headers=self.headers, proxies=self.proxies, stream=True) as response:
                #     for chunk in tqdm(response.iter_content(chunk_size=self.chunk)):
                #         image = Image.open(io.BytesIO(chunk))
                #         image.save(path, "JPEG")
                
            print(f"{type}下载完成！")
        except exceptions.ChunkedEncodingError:
            print(f"网络异常，{path} 下载失败！")
