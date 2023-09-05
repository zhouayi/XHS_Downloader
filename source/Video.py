from re import compile


class Video:
    VIDEO_API = "https://sns-video-bd.xhscdn.com/"
    # VIDEO_ID = compile(r'"masterUrl":"(.*?)"')
    VIDEO_ID = compile(r'"originVideoKey":"(.*?)"')
    

    def get_video_link(self, html: str):
        return self.__get_video_link(html)

    def __get_video_link(self, html: str) -> list:
        return [self.VIDEO_API + self.clean_url(u) for u in self.VIDEO_ID.findall(html)]

    @staticmethod
    def clean_url(url: str) -> str:
        return bytes(url, "utf-8").decode("unicode_escape")
