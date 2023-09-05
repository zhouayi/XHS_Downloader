from source import Settings
from source import XHS


def example():
    """通过代码设置参数，适合二次开发"""
    # 测试链接
    error_demo = "https://www.xiaohongshu.com/explore/"
    image_demo = "https://www.xiaohongshu.com/explore/64eaef33000000000103e75d"
    video_demo = "https://www.xiaohongshu.com/explore/64eb345d000000000800c9ab"
    # 实例对象
    path = "./"  # 作品下载储存根路径，默认值：当前路径
    folder = "Download"  # 作品下载文件夹名称（自动创建），默认值：Download
    proxies = None  # 网络代理
    timeout = 5  # 网络请求超时限制，默认值：10
    chunk = 1024 * 1024  # 下载文件时，每次从服务器获取的数据块大小，单位字节
    xhs = XHS(
        path=path,
        folder=folder,
        proxies=proxies,
        timeout=timeout,
        chunk=chunk, )  # 使用自定义参数
    # xhs = XHS()  # 使用默认参数
    download = True  # 是否下载作品文件
    # 返回作品详细信息，包括下载地址
    print(xhs.extract(error_demo))  # 获取数据失败时返回空字典
    print(xhs.extract(image_demo, download=download))
    print(xhs.extract(video_demo, download=download))

def main():
    xhs = XHS(**Settings().run())
    note_id_list = [
        '64ecb426000000001f03d465',
        '64da4018000000001701ae02'
        ]
    for note_id in note_id_list:
        url = "https://www.xiaohongshu.com/explore/" + note_id
        xhs.extract(url, download=True)

if __name__ == '__main__':
    # example()
    main()
