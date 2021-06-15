import argparse
import numpy as np
import os

from face.recognition import FaceRecognition
from video_getter.video_getter import VideoGetter
from video_process.video_processor import VideoProcessor


def random_pick(length):
    return np.random.randint(0, length)


def download_video(key_word):
    video_getter = VideoGetter(key_word)
    # 只获取一批视频
    video_getter.getVideoFromYoutubeByName(1)
    # 产生可执行文件
    video_getter.generate_cmd("./output/download.sh")
    # 执行可下载脚本
    os.system('chmod +x ./output/download.sh && sh ./output/download.sh')


def split_video(key_word):
    videoDir = "./output/" + key_word

    index = random_pick(len(os.listdir(videoDir)))
    print("正在处理的视频为：" + os.path.join(videoDir, os.listdir(videoDir)[index]))

    video_processor = VideoProcessor(videoSrcPath=os.path.join(videoDir, os.listdir(videoDir)[index]),  # 输入一个视频的绝对路径
                                     videoSavePath=os.path.join('./output/', 'sub_video/'),  # 输入切分后视频的保存路径
                                     videoFrameSavePath="./output/frame/")  # 输入切分后视频的帧的保存路径
    video_processor.videoToSubVideo()
    video_processor.video2frame(320, 240, 1)


def filter_video():
    dirs = os.listdir("./output/frame/")
    for dir in dirs:
        face_recognizer = FaceRecognition(os.path.join("./output/frame/", dir))
        will_delete = face_recognizer.batch_process()
        if will_delete == 1:
            print("删除不符合条件的视频：", "./output/sub_video/" + dir + '.mp4')
            os.remove("./output/sub_video/" + dir + '.mp4')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='爬虫参数')
    parser.add_argument('--key_word', help='视频查询关键词')
    args = parser.parse_args()

    # 下载视频
    print([args.__dict__.get('key_word')])
    download_video([args.__dict__.get('key_word')])

    # 切分视频
    split_video(args.__dict__.get('key_word'))

    # 过滤视频
    filter_video()

    # 剩下的视频就是符合需求的视频
