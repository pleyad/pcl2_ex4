# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import gzip as gz
import re
from typing import BinaryIO, Dict, Iterable


def comment_iterator(infile) -> Iterable[Dict]:
    '''Yields comments as converted json-objects.'''
    for line in infile:
        comment = json.loads(line.decode('utf8'))
        yield comment


def mk_meme_corpus(infile: BinaryIO,
                   outfile: str,
                   min_score: int = 100,
                   min_len: int = 1,
                   max_len: int = 30):
    '''Creates a corpus of comments.'''
    indexset = set()
    outfile = gz.open(outfile, 'wt', encoding='utf8')
    try:
        for comment in comment_iterator(infile):
            text = comment['body']
            ups = comment['score']
            if len(text) > max_len or len(text) < min_len:
                continue
            elif ups < min_score:
                continue

            h_value = hash(text)

            if h_value not in indexset:
                indexset.add(h_value)
                text = re.sub(r'\n', r'\\n', text)
                outfile.write('{}\n'.format(text))
    except KeyboardInterrupt:
        pass
    outfile.close()
