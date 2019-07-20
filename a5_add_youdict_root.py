import re
from find_root import Root

rt = Root()

with open('anki_txt.txt', 'r') as f:
    lines = f.readlines()

new_txt_line_list = []
for line in lines:
    line = line[:-1]
    word = line.split('\\')[0]
    root_list = rt.search(word)
    for root in root_list:
        root = root.strip('\n')
        line += '\\'+root

    line += '\n'
    print(line)
    new_txt_line_list.append(line)

with open('youdict_anki.txt', 'w', encoding='UTF-8') as f:
    for rw in new_txt_line_list:
        f.write(rw)


