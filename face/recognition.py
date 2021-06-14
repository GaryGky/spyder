import os

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
        self.face_square_threshold = 100 * 100

    # 识别并单张图片的计算人脸面积
    def face_calculate(self, pic_path):
        image = face_recognition.load_image_file(pic_path)
        face_location = face_recognition.api.face_locations(image)

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
        for pic in pics:
            pic_path = self.frame_src + pic
            print("正在计算的图片: " + pic_path)

            if not self.face_calculate(pic_path):
                os.remove(self.frame_src)
                break
