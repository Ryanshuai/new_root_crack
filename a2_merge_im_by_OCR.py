import cv2
import pytesseract
import numpy as np
import os
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


def is_same(key_word_0, key_word_1):
    if key_word_1 == key_word_0:
        return True
    if key_word_1.lower() == key_word_0.lower():
        return True
    return False


def find_line(img):
    base_line = np.mean(img[:, 5:10], axis=1)

    diff_line = np.diff(base_line)
    diff_line = abs(diff_line)
    diff_line = (diff_line-5).clip(min=0)

    word_pos_list = list()
    root_pos_list = list()

    i = 0
    while i < len(base_line) - 10:
        if abs(diff_line[i]) > 0:
            if base_line[i+10] < 80:
                word_pos_list.append(i)
                i += 65
            else:
                root_pos_list.append(i)
                i += 65
            # img[i, :] = 255
        i += 1

    # cv2.imshow('', img)
    # cv2.waitKey()

    return word_pos_list, root_pos_list


def word_ocr_by_title_line(title_line, img):
    word_im = img[title_line + 15:title_line + 50, 20:600]
    word_im = 255 - word_im
    ret, word_im = cv2.threshold(word_im, 127, 255, cv2.THRESH_BINARY)
    word = pytesseract.image_to_string(word_im)
    word = word.replace("!", "l")
    # if len(word) == 0:
    #     print(word)
    #     cv2.imshow('word_im', word_im)
    #     cv2.waitKey()
    # if not is_right_word(word):
    #     cv2.imwrite(word+'.jpg', word_im)
    return word, word_im


def root_ocr_by_title_line(title_line, img):
    root_im = img[title_line + 12:title_line + 65, 20:]
    ret, root_im = cv2.threshold(root_im, 60, 255, cv2.THRESH_BINARY)
    root = pytesseract.image_to_string(root_im, lang='chi_sim')
    root = root.replace(' ', '')
    root = root.replace('\n', '')
    return root, root_im


def merge_im_by_title_line(im0, im1, im0_name, im1_name):
    word_pos_list0, _ = find_line(im0)
    word_pos_list1, _ = find_line(im1)
    key_word_1, key_word_1_im = word_ocr_by_title_line(word_pos_list1[0], im1)
    print(im1_name, '  im1:     ', key_word_1)
    correct_set = dict()
    for i in range(len(word_pos_list0)-1, len(word_pos_list0)-15, -1):
        if (im0.shape[0] - word_pos_list0[i]) < 51:
            continue
        key_word_0, key_word_0_im = word_ocr_by_title_line(word_pos_list0[i], im0)
        correct_set[key_word_0] = word_pos_list0[i]
        print('    ', im0_name, '  im0:     ', key_word_0)
        if is_same(key_word_0, key_word_1):
            # diff_length = im0.shape[0] - word_pos_list0[i] + word_pos_list1[0]
            new_im = np.concatenate((im0[:word_pos_list0[i]], im1[word_pos_list1[0]:]))
            return new_im

    manu_word_0 = input('The right word is :')
    new_im = np.concatenate((im0[:correct_set[manu_word_0]], im1[word_pos_list1[0]:]))
    return new_im


def merge_im_under_fold(fold_name, begin=0, end=None):
    if end is None:
        end = len(os.listdir(fold_name))
    res_im = cv2.imread(fold_name + '/' + str(begin) + '.png', 0)
    for i in range(begin+1, end):
        # print(i)
        append_im_name = fold_name + '/' + str(i) + '.png'
        append_im = cv2.imread(append_im_name, 0)

        res_im = merge_im_by_title_line(res_im, append_im, fold_name + '/' + str(i-1) + '.png', append_im_name)

    cv2.imwrite(fold_name + '.png', res_im)
    return res_im


if __name__ == '__main__':

    big_im = merge_im_under_fold(str(5), begin=1355)
    cv2.imwrite(str(5)+'.png', big_im)

    # res_im = cv2.imread('6.png')
    # for i in range(4, 0, -1):
    #     add_im = cv2.imread(str(i)+'.png')
    #     new_im = np.concatenate((res_im, add_im))
    #
    # cv2.imwrite('whole_list.png', res_im)

