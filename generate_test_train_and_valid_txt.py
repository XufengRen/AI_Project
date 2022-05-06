import os

with open('data/train.txt', 'w')as out:
    for images in [f for f in os.listdir('train') if f.endswith('jpg')]:
        out.write('train/' + images + '\n')

import os

with open('data/test.txt', 'w')as out:
    for images in [f for f in os.listdir('test') if f.endswith('jpg')]:
        out.write('test/' + images + '\n')

import os

with open('data/valid.txt', 'w')as out:
    for images in [f for f in os.listdir('valid') if f.endswith('jpg')]:
        out.write('valid/' + images + '\n')