import sys
from PIL import Image
input = sys.argv

print(sys.argv[1])
i=1
while i<len(input):
    try:
        img = Image.open(input[i])
        img.show()
    except IOError:
        pass

    i=i+1