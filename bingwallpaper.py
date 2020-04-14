# -*- coding:utf-8 -*-

import requests
import time
import os
import random
import datetime


def write_log(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        dt = datetime.datetime.now()
        now = dt.strftime("%Y-%m-%d %H:%M:%S")
        msg = now + ': 自动更新壁纸  成功\n'
        res = []
        if not os.path.exists('log.txt'):
            fd = open("log.txt", mode="w", encoding="utf-8")
            fd.close()
        else:
            with open("log.txt", 'r', encoding='utf-8') as f:
                res = f.readlines()
        with open("log.txt", 'w', encoding='utf-8') as f:
            f.write(msg)
            f.writelines(res)

    return inner


class BingWallPaper():
    URL = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=8&mkt=zh-CN'
    HEADERS = {
        'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }
    IMGS_ROOT = os.path.join(os.path.dirname(__file__),
                             'images').replace('\\', '/')

    def __init__(self):
        res = requests.get(BingWallPaper.URL,
                           headers=BingWallPaper.HEADERS).json()
        imgs = res['images']
        self.imgs_url = ['http://www.cn.bing.com' + img['url'] for img in imgs]
        # 如果图片文件夹不存在 则创建
        self.create_images_dir()
        # 清空壁纸图片文件夹
        self.clear_images()
        # 下载壁纸
        self.download()

    @write_log
    def download(self):
        for index, img in enumerate(self.imgs_url):
            content = requests.get(img, headers=BingWallPaper.HEADERS).content
            with open(BingWallPaper.IMGS_ROOT + '/{}.jpg'.format(index + 1),
                      'wb') as f:
                f.write(content)
            time.sleep(random.random())

    @classmethod
    def clear_images(cls):
        if len(os.listdir(cls.IMGS_ROOT)):
            BingWallPaper.clear_dir(cls.IMGS_ROOT)

    @staticmethod
    def clear_dir(dirpath):
        if os.path.isdir(dirpath):
            for fn in os.listdir(dirpath):
                fnpath = os.path.join(dirpath, fn).replace('\\', '/')
                BingWallPaper.clear_dir(fnpath)
        else:
            os.remove(dirpath)

    @classmethod
    def create_images_dir(cls):
        if not os.path.exists(cls.IMGS_ROOT):
            os.mkdir(cls.IMGS_ROOT)


if __name__ == "__main__":
    BingWallPaper()
