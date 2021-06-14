import os

from face.recognition import FaceRecognition
from get_video.video_getter import VideoGetter
from video_process.video_processor import VideoProcessor

key_word = "Europe Cup/"


def download_video():
    video_getter = VideoGetter(key_word)
    # 只获取一批视频
    video_getter.getVideoFromYoutubeByName(1)
    # 产生可执行文件
    video_getter.generate_cmd("./download.sh")
    # 执行可下载脚本
    os.system('chmod +x ./download.sh && sh ./download.sh')


def split_video():
    # TODO: 添加命令行控制
    video_processor = VideoProcessor("视频源地址", './' + key_word + '/', "./frame/")
    video_processor.videoToSubVideo()
    video_processor.video2frame(320, 240, 1)


def filter_video():
    dirs = os.listdir("./frame/")
    for dir in dirs:
        face_recognizer = FaceRecognition(dir)
        face_recognizer.batch_process()


if __name__ == '__main__':
    # 下载视频
    download_video()

    # 切分视频
    split_video()

    # 过滤视频
    filter_video()

    # 剩下的视频就是符合需求的视频
