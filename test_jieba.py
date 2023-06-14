import jieba
from bt_language_parser.parser import *


if __name__ == '__main__':
    sent = "execute a sequence node with child nodes grab_parts, moving_package, and place_package"
    words = jieba.cut(sent, cut_all=False)
    for word in words:
        print(word)