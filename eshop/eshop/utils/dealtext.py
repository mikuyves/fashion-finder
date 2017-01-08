# -*- coding: utf-8 -*-
import re


def match_zh(text):
    # Find out if there is any Chinese character in the text.
    zh_re = re.compile(u'[\u4e00-\u9fa5]+')
    return zh_re.search(text)
