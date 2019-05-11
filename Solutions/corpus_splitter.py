# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import etree
from typing import Any, BinaryIO, Generator
import gzip
import os
import random

BASENAME = 'abstracts.'


def text_iterator(infile: BinaryIO) -> Generator[str]:
    '''Yields lines.'''
    for _, doc in etree.iterparse(infile, tag='document'):
        text = []
        for sentence in doc.iterfind('.//sentence'):
            text.append(sentence.text)

        if len(text) != 0:
            yield ' '.join(text)
        doc.clear()


def split_corpus(infile: BinaryIO, targetdir: str, n: int=1000):
    '''Splits the corpus in test-, dev- and training-set.'''
    k = 2*n
    reservoir = []

    with gzip.open(os.path.join(targetdir, BASENAME + 'training.txt.gz'), 'w') as training:
        reservoir = sample(text_iterator(infile), k, training)

    for i, name in enumerate(['dev', 'test']):
        with gzip.open(os.path.join(targetdir, BASENAME + name + '.txt.gz'), 'w') as f:
            f.writelines([(line + '\n').encode('utf8') for line in reservoir[i::2]])


def sample(collection: Iterable[Any], k: int, outfile: BinaryIO):
    '''
    Perform Knuth's reservoir sampling.

    Returns `k` random elements sampled from a `collection`; all other elements
    are written to `outfile`.
    '''
    reservoir = []
    for t, abstract in enumerate(collection):
        if t < k:
            reservoir.append(abstract)
        else:
            m = random.randint(0, t)
            if m < k:
                abstract, reservoir[m] = reservoir[m], abstract
            outfile.write((abstract + '\n').encode('utf8'))
    return reservoir


def main():
    '''
    Run as script.
    '''
    with gzip.open('petit_abstracts.xml.gz', mode='rb') as f:
        split_corpus(f, 'ausgabe_a2', 30)


if __name__ == '__main__':
    main()
