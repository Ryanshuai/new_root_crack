import re
import bs4.element
from bs4 import BeautifulSoup


def re_one_line(soup):
    pos = re.search(r'.*?\t', soup.text).span()
    root_txt = soup.text[pos[0]: pos[1]]
    root_txt = re.sub(r'\(.\)', ' ', root_txt, count=0, flags=0)
    root_txt = re.sub(r'\[.*\]', ' ', root_txt, count=0, flags=0)
    root_txt = re.sub(r'[\u4e00-\u9fa5]', ' ', root_txt, count=0, flags=0)
    root_txt = root_txt.replace('-', ' ')
    root_txt = root_txt.replace('(', ' ')
    root_txt = root_txt.replace(')', ' ')
    root_txt = root_txt.replace(',', ' ')
    root_txt = root_txt.replace(';', ' ')
    root_list = root_txt.split()

    return root_list


def is_word_in_page(word, page_soup):
    if word not in page_soup.text:
        return False

    root_list = re_one_line(page_soup)
    for root in root_list:
        if root in word:
            return True
    return False


def is_root_same(A, B):
    a = re_one_line(A)
    b = re_one_line(B)
    if len(set(a).intersection(set(b))) == 0:
        return False
    return True


def delete_intersection(page_soup_list):
    i = 0
    while i < len(page_soup_list):
        j = i + 1
        while j < len(page_soup_list):
            if is_root_same(page_soup_list[i], page_soup_list[j]):
                del page_soup_list[j]
                continue
            j = j + 1
        i = i + 1
    return page_soup_list


def find_which_page(word, txt_lines):
    page_soup_list = list()
    for line in txt_lines:
        page_soup = BeautifulSoup(line, 'html.parser', from_encoding='utf-8')
        if is_word_in_page(word, page_soup):
            page_soup_list.append(page_soup)

    page_soup_list = delete_intersection(page_soup_list)

    return page_soup_list


########################################################################################################################

def is_mode_1(soup):
    return '【同源单词】' in soup.contents[len(soup.contents) - 2].text


def process_mode_1(soup):
    root = soup.contents[2].text
    for i in range(2, len(soup.contents) - 1):
        if '【来源及含义】' in soup.contents[i].text:
            root += soup.contents[i].text
        if '【词根含义】' in soup.contents[i].text:
            root += soup.contents[i].text
        if '【词根来源】' in soup.contents[i].text:
            root += soup.contents[i].text
    return root


def is_mode_2(soup):
    contents = filter(lambda x: isinstance(x, bs4.element.Tag), soup.contents)
    for con in contents:
        if '同源词：' in con.text:
            return True
    return False


def process_mode_2(soup):
    pos = re.search(r'.*?同源词', soup.text).span()
    root = soup.text[pos[0]: pos[1]][:-3]
    return root


def is_mode_3(soup):
    if '①' in soup.contents[3].text[0:3]:
        return True
    if '1、' in soup.contents[3].text[0:3]:
        return True
    return False


def has_number(con):
    for i in range(0, 10):
        if str(i) in con.text[0:2]:
            return True
    return False


def has_circle_number(con):
    if '①' in con.text:
        return True
    if '②' in con.text:
        return True
    if '③' in con.text:
        return True
    if '缀：' in con.text:
        return True
    return False


def process_mode_3(word, soup):
    root = ''
    no_num_show = True
    no_circle_show = True
    start_flag = False
    root_list = list()
    contents = list(filter(lambda x: isinstance(x, bs4.element.Tag), soup.contents))
    for i in range(len(contents)-1, 0, -1):
        con = contents[i]

        if word in con.text:
            start_flag = True
        elif start_flag:
            if has_number(con) and no_num_show:
                root_list.append(con.text)
                no_num_show = False
            if has_circle_number(con) and no_circle_show:
                root_list.append(con.text)
                no_circle_show = False

    for i in range(len(root_list) - 1, -1, -1):
        root += root_list[i]
    return root


def is_mode_4(soup):
    # print((soup.contents[2].text.split()[0]))
    return not (soup.contents[2].text.split()[0]).isalpha()


def process_mode_4(soup):
    root = soup.contents[2].text
    if not soup.contents[3].text.split()[0].isalpha():
        root += soup.contents[3].text
    return root


class Root:
    def __init__(self):
        with open('youdict_utf8.txt', 'r', encoding='UTF-8') as f:
            self.txt_lines = f.readlines()

    def search(self, word):
        root_list = list()

        page_soup_list = find_which_page(word, self.txt_lines)

        for page_soup in page_soup_list:

            if is_mode_1(page_soup):
                # for con in page_soup.contents:
                #     if isinstance(con, bs4.element.Tag):
                #         print(con.text)
                root = process_mode_1(page_soup)
                root_list.append(root)

            elif is_mode_2(page_soup):
                root = process_mode_2(page_soup)
                root_list.append(root)

            elif is_mode_3(page_soup):
                root = process_mode_3(word, page_soup)
                root_list.append(root)

            elif is_mode_4(page_soup):
                root = process_mode_4(page_soup)
                root_list.append(root)
        return root_list


if __name__ == '__main__':
    rt = Root()
    rt.search('agonize')


