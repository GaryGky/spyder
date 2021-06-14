## 需求

输入：一个关键字；

输出：一个视频的列表；

## 实现流程

1. 先用关键字去爬取YouTube五分钟内的视频，将视频保存至本地；
2. 对于其中一个视频而言，按照如下方法进行计算：
   1. 子视频：使用FFmpeg或者OpenCV对其进行分帧（假设10秒一帧），这一步可以得到一个子视频的临时文件夹；
   2. 抽取：对于每一个子视频抽帧，这一步可以得到一个临时帧数组；
   3. 识别：对每一帧进行人脸识别，得到一个bbox，计算该bbox的面积，近似于人脸面积。
   4. 判断：对于每一帧，计算其人脸大小面积是否全部超过设定的阈值，假设为：10cm2；
   5. 持久化：对于符合条件的帧，保存到本地；

## 技术栈

- 面向YouTube爬虫（selenium）
- OpenCV分帧（cv2）
- 人脸识别API: 使用开源库：`face_recognition`对图像中的人脸进行检测和定位：https://github.com/ageitgey/face_recognition/blob/master/README_Simplified_Chinese.md

## 遇到问题

#### FFMPEG无法解码：

```
FFMPEG: tag 0x47504a4d/'MJPG' is not supported with codec id 7 and format 'mp4 / MP4 (MPEG-4 Part 14)
```

解决：转换成mp4v即可；



## GitHub

https://github.com/GaryGky/spyder