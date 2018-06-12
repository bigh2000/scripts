# 어노테이션 파일(anno_root/json_name)을 읽어들여
# 한글(0,1,2,3,4,5), 자모(6), 알파벳(7), 숫자(8), 기타(9)로 class_num을 분류하고
# 예외처리(10000) 한 뒤
# console에 Caption과 class_num을 출력하고
# train set과 val set을 9:1의 비율로 랜덤하게 선정해
# anno_root/dir_name 밑에 caption_train.txt와 caption_val.txt로 저장한다.
import os
import argparse
import json
import cv2
import random
import hgtk
"""
Class_Map
0 : 가
1 : 고
2 : 과
3 : 각
4 : 곡
5 : 곽
6 : ㄱ
7 : a
8 : 1
9 : !
"""
CHO = (
    u'ㄱ', u'ㄲ', u'ㄴ', u'ㄷ', u'ㄸ', u'ㄹ', u'ㅁ', u'ㅂ', u'ㅃ', u'ㅅ',
    u'ㅆ', u'ㅇ', u'ㅈ', u'ㅉ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ'
)
JOONG = (
    u'ㅏ', u'ㅐ', u'ㅑ', u'ㅒ', u'ㅓ', u'ㅔ', u'ㅕ', u'ㅖ', u'ㅣ',  # 길쭉이 0 ~ 8
    u'ㅗ', u'ㅜ', u'ㅛ', u'ㅠ', u'ㅡ',                             # 넓쩍이 9 ~ 13
    u'ㅘ', u'ㅙ', u'ㅚ', u'ㅝ', u'ㅞ', u'ㅟ', u'ㅢ'                # 길넓이 14 ~ 20
)
JONG = (
    u'', u'ㄱ', u'ㄲ', u'ㄳ', u'ㄴ', u'ㄵ', u'ㄶ', u'ㄷ', u'ㄹ', u'ㄺ',
    u'ㄻ', u'ㄼ', u'ㄽ', u'ㄾ', u'ㄿ', u'ㅀ', u'ㅁ', u'ㅂ', u'ㅄ', u'ㅅ',
    u'ㅆ', u'ㅇ', u'ㅈ', u'ㅊ', u'ㅋ', u'ㅌ', u'ㅍ', u'ㅎ'
)
JAMO = CHO + JOONG + JONG[1:]
FIRST_HANGUL_UNICODE = 0xAC00  # '가'
LAST_HANGUL_UNICODE = 0xD7A3  # '힣'
FIRST_NUMBER_UNICODE = 0x0030  # '0'
LAST_NUMBER_UNICODE = 0x0039  # '9'
FIRST_ALPHABET_UPPER_UNICODE = 0x0041  # 'A'
LAST_ALPHABET_UPPER_UNICODE = 0x005A  # 'Z'
FIRST_ALPHABET_LOWER_UNICODE = 0x0061  # 'a'
LAST_ALPHABET_LOWER_UNICODE = 0x007A  # 'z'
def is_jamo(letter):
    return letter in JAMO
def is_hangul(phrase): # TODO: need tuning!!
    for letter in phrase:
        code = ord(letter)
        if (code < FIRST_HANGUL_UNICODE or code > LAST_HANGUL_UNICODE) and not is_jamo(letter):
            return False
    return True
def is_alphabet(phrase): # TODO: need tuning!!
    unicode_value = ord(phrase)
    if (unicode_value >= FIRST_ALPHABET_UPPER_UNICODE and unicode_value <= LAST_ALPHABET_UPPER_UNICODE) \
       or (unicode_value >= FIRST_ALPHABET_LOWER_UNICODE and unicode_value <= LAST_ALPHABET_LOWER_UNICODE):
        return True
    else:
        return False
def is_number(phrase): # TODO: need tuning!!
    for letter in phrase:
        code = ord(letter)
        if (code < FIRST_NUMBER_UNICODE or code > LAST_NUMBER_UNICODE):
            return False
    return True
def class_assign(caption):
    if len(caption) == 1:
        if is_hangul(caption):
            if is_jamo(caption):
                if caption in result_dict['hangul_jamo']:
                    result_dict['hangul_jamo'][caption] += 1
                else:
                    result_dict['hangul_jamo'][caption] = 1
                class_num = 6
            else:
                if caption in result_dict['hangul']:
                    result_dict['hangul'][caption] += 1
                else:
                    result_dict['hangul'][caption] = 1
                eumso_list = hgtk.letter.decompose(caption)
                middle_sung = eumso_list[1]
                last_sung = eumso_list[2]
                if last_sung == JONG[0]:
                    if middle_sung in JOONG[:9]:
                        class_num = 0
                    elif middle_sung in JOONG[9:14]:
                        class_num = 1
                    elif middle_sung in JOONG[14:]:
                        class_num = 2
                elif last_sung in JONG[1:]:
                    if middle_sung in JOONG[0:9]:
                        class_num = 3
                    elif middle_sung in JOONG[9:14]:
                        class_num = 4
                    elif middle_sung in JOONG[14:]:
                        class_num = 5
                else:
                    raise ValueError
        elif is_alphabet(caption):
            if caption in result_dict['alphabet']:
                result_dict['alphabet'][caption] += 1
            else:
                result_dict['alphabet'][caption] = 1
            class_num = 7
        elif is_number(caption):
            if caption in result_dict['number']:
                result_dict['number'][caption] += 1
            else:
                result_dict['number'][caption] = 1
            class_num = 8
        else:
            if caption in result_dict['etc']:
                result_dict['etc'][caption] += 1
            else:
                result_dict['etc'][caption] = 1
            class_num = 9
    else:
        if caption in result_dict['non_single']:
            result_dict['non_single'][caption] += 1
        else:
            result_dict['non_single'][caption] = 1
        class_num = 10000
        if caption == '...':
            class_num = 9
    return class_num
if __name__=='__main__':
    json_name = 'ocr_demo2.json'
    dir_name = os.path.splitext(json_name)[0]+'_cap'
    parser = argparse.ArgumentParser()
    parser.add_argument("--anno_root", type=str, default="/home/vdo-data3/Project/Data")
    args = parser.parse_args()
    anno_root = args.anno_root
    if not os.path.exists(os.path.join(anno_root, dir_name)):
        os.mkdir(os.path.join(anno_root, dir_name))
    with open(os.path.join(anno_root, json_name)) as f:
        anno = json.load(f)
    f_1 = open(os.path.join(anno_root, dir_name, 'caption_train.txt'), 'w')
    f_2 = open(os.path.join(anno_root, dir_name, 'caption_val.txt'), 'w')
    result_dict = dict()
    result_dict['hangul'] = dict()
    result_dict['hangul_jamo'] = dict()
    result_dict['number'] = dict()
    result_dict['alphabet'] = dict()
    result_dict['etc'] = dict()
    result_dict['non_single'] = dict()
    count = 0
    for clip in anno['annotation']['clips']:
        clip_name = clip['clip_name']
        for image in clip['images']:
            divider = True if random.randrange(1, 10) > 1 else False
            if divider:
                f = f_1
            else:
                f = f_2
            image_name = image['filename']
            im = cv2.imread(os.path.join(anno_root, dir_name, clip_name, image_name))
            image_path = os.path.join(clip_name,image_name)
            f.write(image_path)
            for bbox in image['bbox']:
            #     x1 = int(bbox['start_x'])
            #     x2 = int(bbox['end_x'])
            #     y1 = int(bbox['start_y'])
            #     y2 = int(bbox['end_y'])
            #
            #     cls = str(bbox['caption'])
            #     cv2.rectangle(im,(x1,y1),(x2,y2),(0,255,0),2)
            #     cv2.putText(im, cls, (x1,y1), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.4, (0,255,0))
            #
            # cv2.imshow('photo', im)
            # cv2.waitKey(0)
                # class number assign with caption
                caption = bbox['caption']
                class_num = class_assign(caption)
                if class_num == 10000:
                    continue
                bbox_xyxy = bbox['position']
                for coord in bbox_xyxy:
                    coord = str(int(coord))
                    f.write(' ' + coord)
                f.write(' {}'.format(class_num))
                print('Caption : {} | class_num : {}'.format(caption, class_num))
            f.write('\n')
            count += 1
            print('{} processed'.format(count))
    f_1.close()
    f_2.close()
    print('done')