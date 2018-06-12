# path_base의 하위 폴더를 정렬하여 dirs에 저장하고
# 이를 이용하여 path_write 하위에 동영상마다 한 폴더씩 이미지를 frame 단위로 추출해 저장한 뒤
# 동영상과 폴더간의 대응관계를 name_json에 저장한다.
import cv2
import json
import os

from collections import OrderedDict
from natsort import natsorted
from os.path import exists, join

num_frame = 5
path_base = '/home/vdo-data3/Project/Data/test_vdos'
path_write = path_base + '_img'
if not exists(path_write):
    os.mkdir(path_write)
dirs = natsorted([f for f in os.listdir(path_base)])

cnt_folder = -1
dict = OrderedDict()

for i, dir in enumerate(dirs):
    path = join(path_base, dir)
    vdos = natsorted([v for v in os.listdir(path)])
    if vdos[-1][:-4] == vdos[0][:-8]:
        vdos.insert(0, vdos[-1])
        del vdos[-1]
    print(i, dir, vdos)

    for j, vdo in enumerate(vdos):
        cnt_frame = 0
        cnt_folder += 1
        if not exists(join(path_write, '%06d' % cnt_folder)):
            os.mkdir(join(path_write, '%06d' % cnt_folder))
        cap = cv2.VideoCapture(join(path, vdo))
        while True:
            dict['%06d' % cnt_folder] = join(dir, vdo)
            ret, frame = cap.read()
            if ret is False:
                break
            if cnt_frame % num_frame == 0:
                cv2.imwrite(join(join(path_write, '%06d' % cnt_folder), '%04d' % int(cnt_frame / num_frame) + '.jpg'), frame)
            flag = True
            cnt_frame += 1
name_json = path_base.split('/')[-1]+'_dict.json'
file = open(join(join(path_base, '..'), name_json), 'w')
file.write(json.dumps(dict, ensure_ascii=False))