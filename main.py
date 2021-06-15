import argparse
import os

from face.recognition import FaceRecognition
from video_getter.video_getter import VideoGetter
from video_process.video_processor import VideoProcessor


def download_video(key_word):
    video_getter = VideoGetter(key_word)
    # 只获取一批视频
    video_getter.getVideoFromYoutubeByName(1)
    # 产生可执行文件
    video_getter.generate_cmd("./download.sh")
    # 执行可下载脚本
    os.system('chmod +x ./download.sh && sh ./download.sh')


def split_video(key_word):
    videoDir = "./" + key_word
    print("正在处理的视频为：" + os.path.join(videoDir, os.listdir(videoDir)[0]))
    video_processor = VideoProcessor(videoSrcPath=os.path.join(videoDir, os.listdir(videoDir)[0]),  # 输入一个视频的绝对路径
                                     videoSavePath='./' + key_word + '/',  # 输入切分后视频的保存路径
                                     videoFrameSavePath="./frame/")  # 输入切分后视频的帧的保存路径
    video_processor.videoToSubVideo()
    video_processor.video2frame(320, 240, 1)


def filter_video():
    dirs = os.listdir("./frame/")
    for dir in dirs:
        face_recognizer = FaceRecognition(dir)
        face_recognizer.batch_process()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='爬虫参数')
    parser.add_argument('--key_word', help='视频查询关键词')
    args = parser.parse_args()

    # # 下载视频
    # print([args.__dict__.get('key_word')])
    # download_video([args.__dict__.get('key_word')])

    # 切分视频
    split_video(args.__dict__.get('key_word'))

    # 过滤视频
    filter_video()

    # 剩下的视频就是符合需求的视频
