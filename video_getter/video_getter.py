import os

from selenium import webdriver
import time
from bs4 import BeautifulSoup


class VideoGetter:
    driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
    video_id_list = []
    video_path = ''
    key_word = []

    def __init__(self, key_word):
        self.driver.get("https://www.youtube.com/")
        self.video_path = os.path.join('./output/', key_word[0])
        self.key_word = key_word

    def execute_limit(self, limit):
        for i in range(limit):
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            zzr = soup.find_all('a', id="thumbnail")

            for item in zzr:
                video = item.get("href")
                if video is not None and "/watch?v=" in video:
                    video_id = video.replace('/watch?v=', '')
                    print(video_id)
                    self.video_id_list.append(video_id)

            js = "var q=document.documentElement.scrollTop=100000000000"
            self.driver.execute_script(js)
            time.sleep(3)  # 等待页面刷新

    def getVideoFromYoutubeByName(self, limit):
        self.driver.maximize_window()
        time.sleep(1)
        self.driver.refresh()
        self.driver.get_cookies()

        for query in self.key_word:
            # 视频时长小于4分钟
            url = 'https://www.youtube.com/results?search_query=' + query + '&sp=EgQQARgB'
            self.driver.get(url)
            print(query)

            self.execute_limit(limit)
            time.sleep(1)

        self.driver.quit()

    def generate_cmd(self, output_filename='download.sh'):
        filename = os.path.join(self.video_path, "v_%s.mp4")
        cmd_base = "youtube-dl -f best -f mp4 "
        cmd_base += '"https://www.youtube.com/watch?v=%s" '
        cmd_base += '-o "%s"' % filename

        cnt = 0
        with open(output_filename, "w") as fobj:
            for vid in self.video_id_list:
                cmd = cmd_base % (vid, vid)
                fobj.write("%s\n" % cmd)

                # Debug: 限制最多只拉3个视频
                cnt += 1
                if cnt >= 3:
                    break


if __name__ == '__main__':
    video_getter = VideoGetter(["Biden"])
    video_getter.getVideoFromYoutubeByName(1)
    print(video_getter.video_id_list)
    video_getter.generate_cmd('./output/download.sh')
    os.system('chmod +x ./output/download.sh && sh ./output/download.sh')
