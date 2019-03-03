import cv2
import pytesseract
import numpy as np
import os
import json
from autocorrect import spell


def is_right_word(word):
    if len(word) == 0:
        return False
    word_list = '-abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for i in word:
        if i not in word_list:
            return False
    if spell(word) != word:
        return False
    return True


def word_ocr_by_title_line(title_line, img, im_No, k_in_list, last_word):
    word_im = img[title_line + 15:title_line + 50, 15:600]
    word_im = 255 - word_im
    ret, word_im = cv2.threshold(word_im, 127, 255, cv2.THRESH_BINARY)
    word = pytesseract.image_to_string(word_im)
    word = word.replace("!", "l")
    if not is_right_word(word):
        cv2.imwrite('check_image/im'+str(im_No)+'__line_'+str(k_in_list)+'__word_'+word+'__lastword_'+str(last_word)+'.png', word_im)
    return word, word_im


def root_ocr_by_title_line(title_line, img):
    root_im = img[title_line + 12:title_line + 65, 15:]
    ret, root_im = cv2.threshold(root_im, 60, 255, cv2.THRESH_BINARY)
    root = pytesseract.image_to_string(root_im, lang='chi_sim')
    root = root.replace(' ', '')
    root = root.replace('\n', '')
    root = root.replace('\n', '')
    return root, root_im


def generate_root_word_list(img, im_No):
    root_word_list = list()

    base_line = np.mean(img[:, 5:10], axis=1)

    diff_line = np.diff(base_line)
    diff_line = abs(diff_line)
    diff_line = (diff_line-10).clip(min=0)

    k_in_list = 0
    i = 0
    last_word = None
    while i < len(base_line) - 50:
        if abs(diff_line[i]) > 0:
            if base_line[i + 10] > 80:  # root line
                root, root_im = root_ocr_by_title_line(i, img)
                root_word_list.append('<<'+root+'>>')
                print('<<'+root+'>>')
                # print(root)
                # cv2.imshow('root_im', root_im)
                # cv2.waitKey()
                k_in_list += 1
                i += 65
            else:   # word line
                word, word_im = word_ocr_by_title_line(i, img, im_No, k_in_list, last_word)
                last_word = word
                root_word_list.append(word)
                print(word)
                # cv2.imshow('word_im', word_im)
                # cv2.waitKey()
                k_in_list += 1
                i += 65

        i += 1

    return root_word_list


if __name__ == '__main__':

    root_word_list = []
    for im_No in range(6, -1, -1):
        img = cv2.imread(str(im_No)+'.png', 0)
        root_word_list = root_word_list + generate_root_word_list(img, im_No)

    # im_No = 0
    # img = cv2.imread(str(im_No) + '.png', 0)
    # root_word_list = root_word_list + generate_root_word_list(img, im_No)

    with open('root_proto.txt', 'a') as f:
        for rw in root_word_list:
            f.write(rw)
            f.write('\n')

