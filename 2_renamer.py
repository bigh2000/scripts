# path_base의 하위폴더를 정렬하여 dirs에 저장하고
# dirs의 모든 하위폴더의 이미지들이 숫자로만 이루어져있다는 가정(Assumption)하에
# 0을 포함한 6자리로 저장한다.
import os

from natsort import natsorted
from os.path import join, splitext

path_base = '/home/vdo-data3/Project/Data/test_imgs_to_rename'
dirs = natsorted([d for d in os.listdir(path_base)])

for d in dirs:
    files = natsorted([f for f in os.listdir(join(path_base, d))])
    for f in files:
        os.chdir(join(path_base, d))
        os.system('mv '+f+' %06d.jpg' % int(splitext(f)[0]))