import cv2
import pytesseract
import numpy as np
import re


# word = '<<94〔32〕′Secut-,sequ-〔32〕,sU-:=folloW,旱琶示“罡艮B迢”o>>'
word = '<<60[46].spect-[12].,spic-:=...丁语。引申为"光谱"。>>'

if '<<' in word:
    if '].' in word:
        word = re.sub(r"<<.*?]", "<<", word)
    else:
        word = re.sub(r"<<.*?〕", "<<", word)
    word = re.sub(r"<<,", "<<", word)
    word = re.sub(r"<<\.", "<<", word)
    word = re.sub(r"<<′", "<<", word)
    word = re.sub(r"<<'", "<<", word)
print(word)
