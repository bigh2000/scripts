import os
from icrawler.builtin.google import GoogleImageCrawler

max_num = 100
data_root = '/home/vdo-data3/Project/Data/celeb'
if not os.path.exists(data_root):
    os.mkdir(data_root)

celeb_name = '여자친구'
celeb_folder = os.path.join(data_root, celeb_name)
if not os.path.exists(celeb_folder):
    os.mkdir(celeb_folder)

google_crawler = GoogleImageCrawler(storage={'root_dir': celeb_folder})
google_crawler.crawl(keyword=celeb_name, max_num=max_num)