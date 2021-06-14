import os

import cv2


class VideoProcessor:
    videoSrcPath = ''
    videoSavePath = ''
    framesSavePath = ''

    def __init__(self, videoSrcPath, videoSavePath, videoFrameSavePath):
        self.videoSrcPath = videoSrcPath
        self.videoSavePath = videoSavePath
        self.framesSavePath = videoFrameSavePath

        if not os.path.exists(self.videoSavePath):
            os.mkdir(self.videoSavePath)

        if not os.path.exists(self.framesSavePath):
            os.mkdir(self.framesSavePath)

    def videoToSubVideo(self):
        # 读入视频文件
        video_capture = cv2.VideoCapture(self.videoSrcPath)

        # FPS
        fps = video_capture.get(5)
        print(video_capture.isOpened())
        print("fps", video_capture.get(5))

        # 总帧数
        print("COUNT", video_capture.get(7))

        # 视频的宽和高
        size = (int(video_capture.get(3)), int(video_capture.get(4)))

        # 每隔10秒截取一段
        interval = 10

        # 当前帧
        frame_index = 0

        # 当前截取的第几段
        flag = 0

        success, bgr_image = video_capture.read()
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        v = cv2.VideoWriter(self.videoSavePath + str(frame_index // (fps * interval)) + '.mp4', fourcc, fps, size)
        while success:  # 循环读取视频帧
            if (frame_index // (fps * interval)) % 2 == 0:
                if v.isOpened():
                    v.write(bgr_image)

            if frame_index == (fps * interval) * flag * 2 + (fps * interval):
                if v.isOpened():
                    v.release()

            if frame_index == (fps * interval) * flag * 2:
                v = cv2.VideoWriter(self.videoSavePath + str(frame_index // (fps * interval)) + '.mp4', fourcc, fps,
                                    size)
                flag += 1

                print("save: %d" % flag)
            success, bgr_image = video_capture.read()
            frame_index = frame_index + 1

        video_capture.release()
        v.release()

    def video2frame(self, frame_width, frame_height, interval):
        videos = os.listdir(self.videoSavePath)
        for each_video in videos:
            print("正在读取视频：", each_video)  # 我的是Python3.6

            each_video_name = each_video[:-4]
            if not os.path.exists(self.framesSavePath + each_video_name):
                os.mkdir(self.framesSavePath + each_video_name)

            # 保存路径
            each_video_save_full_path = os.path.join(self.framesSavePath, each_video_name) + "/"

            # 文件路径
            each_video_full_path = os.path.join(self.videoSavePath, each_video)

            cap = cv2.VideoCapture(each_video_full_path)
            frame_index = 0
            frame_count = 0
            if cap.isOpened():
                success = True
            else:
                success = False
                print("读取失败!")

            while success:
                success, frame = cap.read()
                print("---> 正在读取第%d帧:" % frame_index, success)  # 我的是Python3.6

                if frame_index % interval == 0 and success:  # 如路径下有多个视频文件时视频最后一帧报错因此条件语句中加and success
                    resize_frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
                    cv2.imwrite(each_video_save_full_path + "%d.jpg" % frame_count, resize_frame)
                    frame_count += 1

                frame_index += 1

            cap.release()


if __name__ == '__main__':
    video_processor = VideoProcessor('/Users/bytedance/PycharmProjects/demo/data/v_44HjBgacy1Y.mp4',
                                     './key_word/',
                                     './frame/')
    video_processor.videoToSubVideo()
    video_processor.video2frame(320, 240, 1)