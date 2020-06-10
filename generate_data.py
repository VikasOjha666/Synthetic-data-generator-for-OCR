#Generates data for text detection.

import numpy as np
import argparse
from PIL import Image,ImageDraw,ImageFilter
import random
import os

#Variables declaration.
file_count=0

global x_ptr,y_ptr
x_ptr=0
y_ptr=0
word_lengths=[2,3,4,5]
coor_list=[]

upper_char_list=[]
lower_char_list=[]


parser=argparse.ArgumentParser()
parser.add_argument('--n_samples',type=int,help='No of images to generate.',default=1)
parser.add_argument('--continuos',type=int,help='Whether to put random chars or word based.',default=1)
parser.add_argument('--char_type',type=int,help='1 for all letters are capital 2 for all small and 3 for mix and 4 for capital at start.',
                    default=1)
args=parser.parse_args()


background=Image.open('./background/background.jpg')
blank=Image.open('./objects/blank.png')

upper_letters_name=os.listdir('./objects/upper/')
for filename in upper_letters_name:
    upper_char_list.append(Image.open('./objects/upper/'+filename))

lower_letters=os.listdir('./objects/lower/')
for filename in lower_letters:
    lower_char_list.append(Image.open('./objects/lower/'+filename))


both_char_list=[]
both_char_list.extend(upper_char_list)
both_char_list.extend(lower_char_list)





for _ in range(args.n_samples):
    back_copy=background.copy()
    while True:
        if x_ptr>=900:
            x_ptr=0
            y_ptr+=100
        elif y_ptr>=900:
            back_copy.save('./generated_images/'+str(file_count)+'.jpg')
            file_count+=1
            break

        else:
            word_len=random.choice(word_lengths)
            for j in range(word_len):
                if x_ptr>=900:
                    pass
                else:
                    if args.char_type==1:
                        background.paste(random.choice(upper_char_list),(x_ptr+25,y_ptr))
                    elif args.char_type==2:
                        background.paste(random.choice(lower_char_list),(x_ptr+25,y_ptr))
                    elif args.char_type==4 and x_ptr==0:
                        background.paste(random.choice(upper_char_list),(x_ptr+25,y_ptr))
                    elif args.char_type==3:
                        background.paste(random.choice(both_letters),(x_ptr+25,y_ptr))
                    else:
                        pass



                    coor_list.append([x_ptr+25,y_ptr,x_ptr+25+25,y_ptr+25])
                    x_ptr+=26



            for i in range(3):
                if x_ptr>=1000:
                    pass
                else:
                    background.paste(blank,(x_ptr+25,y_ptr))
                    x_ptr+=26

print(f'Sucessfully generated {args.n_samples}')
