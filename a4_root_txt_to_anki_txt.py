import os
import re

filter_txt_list = list()

for file in os.listdir('filter'):
    with open('filter/'+file, 'r') as f:
        filter_txt_list += f.read().splitlines()

with open('root.txt', 'r') as f:
    root_txt_list = f.read().splitlines()

now_root = None
for i, word in enumerate(root_txt_list):
    if '<<' in word:
        if '].' in word:
            word = re.sub(r"<<.*?]", "<<", word)
        else:
            word = re.sub(r"<<.*?〕", "<<", word)
        word = re.sub(r"<<,", "<<", word)
        word = re.sub(r"<<\.", "<<", word)
        word = re.sub(r"<<′", "<<", word)
        word = re.sub(r"<<'", "<<", word)

        now_root = word[2:-2]
        continue

    root_txt_list[i] = root_txt_list[i]+'\\'+now_root

anki_txt_list = list()
for i, word in enumerate(root_txt_list):
    if word.split('\\')[0] in filter_txt_list:
        anki_txt_list.append(word)
        filter_txt_list.remove(word.split('\\')[0])

with open('anki_txt.txt', 'w') as f:
    for rw in anki_txt_list:
        f.write(rw)
        f.write('\n')

print('following is not include: total: '+str(len(filter_txt_list)))
for i in filter_txt_list:
    print(i)
