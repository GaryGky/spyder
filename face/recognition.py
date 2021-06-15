import os
import shutil

import face_recognition


class FaceRecognition:
    # 要识别的子视频的帧
    frame_src = ''
    # 该子视频是否满足要求: 满足-> 保留；否则删除
    is_satisfaction = True
    # 阈值
    face_square_threshold = 0

    def __init__(self, frame_src):
        self.frame_src = frame_src
        self.face_square_threshold = 10 * 10

    # 识别并单张图片的计算人脸面积
    def face_calculate(self, pic_path):
        image = face_recognition.load_image_file(pic_path)
        face_location = face_recognition.api.face_locations(image)
        print(face_location)

        if len(face_location) == 0:
            self.is_satisfaction = False
            return False

        def square(face_coordinate):
            return abs(face_coordinate[0] - face_coordinate[2]) * abs(face_coordinate[1] - face_coordinate[3])

        if square(face_location[0]) < self.face_square_threshold:
            self.is_satisfaction = False
            return False

        return True

    # 识别一个frame文件夹下的所有图片
    def batch_process(self):
        pics = os.listdir(self.frame_src)
        will_delete = 0
        for pic in pics:
            pic_path = self.frame_src + '/' + pic
            print("正在计算的图片: " + pic_path)

            if not self.face_calculate(pic_path):
                will_delete = 1
                break
        if will_delete == 1:
            shutil.rmtree(self.frame_src)
        return will_delete


def TestFaceCalculate():
    fr = FaceRecognition("")
    res = fr.face_calculate("/Users/bytedance/PycharmProjects/demo/video_process/frame/12.0/0.jpg")
    print(res)


def TestBatchProcess():
    Dir = "/Users/bytedance/PycharmProjects/demo/output/frame/"
    videoDir = "/Users/bytedance/PycharmProjects/demo/output/sub_video/"
    dirs = os.listdir(Dir)
    for dir in dirs:
        print("正在计算的目录: " + Dir + dir)
        face_recogizer = FaceRecognition(Dir + dir)
        will_delete = face_recogizer.batch_process()
        if will_delete == 1:
            os.remove(videoDir + dir + '.mp4')
        print(face_recogizer.is_satisfaction)


if __name__ == '__main__':
    TestBatchProcess()
