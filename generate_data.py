#Generates data for text detection.

import numpy as np
import argparse
from PIL import Image,ImageDraw,ImageFilter
import random
import os

#Variables declaration.
file_count=0

global x_ptr,y_ptr,advance
x_ptr=0
y_ptr=0
word_lengths=[2,3,4,5]
coor_list=[]

upper_char_list=[]
lower_char_list=[]
advance=25
image_sizes=[5,10,15,20,25,30,35,40,45,50]

def resize_images(arr,new_size):
    new_arr=[img.resize(new_size,new_size) for img in arr]
    return new_arr

parser=argparse.ArgumentParser()
parser.add_argument('--n_samples',type=int,help='No of images to generate.',default=1)
parser.add_argument('--continuos',type=int,help='Whether to put random chars or word based.',default=1)
parser.add_argument('--char_type',type=int,help='1 for all letters are capital 2 for all small and 3 for mix and 4 for capital at start.',
                    default=1)
parser.add_argument('--same_sizes',type=int,help='1 for same_size 2 for different_sizes')
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
    upper_char_list_c=upper_char_list.copy()
    lower_char_list_c=lower_char_list_c.copy()
    both_char_list_c=both_char_list_c.copy()
    blank_c=blank.copy()

    if args.same_size==0:
        new_size=random.choice(image_sizes)
        upper_char_list_c=resize_images(upper_char_list_c,new_size)
        lower_char_list_c=resize_images(lower_char_list_c,new_size)
        both_char_list_c=resize_images(both_char_list_c,new_size)
        blank_c=blank_c.resize(new_size,new_size)

    while True:
        if x_ptr>=900:
            x_ptr=0
            y_ptr+=advance*4
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
                        background.paste(random.choice(upper_char_list_c),(x_ptr+advance,y_ptr))
                    elif args.char_type==2:
                        background.paste(random.choice(lower_char_list_c),(x_ptr+advance,y_ptr))
                    elif args.char_type==4 and x_ptr==0:
                        background.paste(random.choice(upper_char_list_c),(x_ptr+advance,y_ptr))
                    elif args.char_type==3:
                        background.paste(random.choice(both_letters_c),(x_ptr+advance,y_ptr))
                    else:
                        pass



                    coor_list.append([x_ptr+advance,y_ptr,x_ptr+advance+advance,y_ptr+advance])
                    x_ptr+=advance+1



            for i in range(3):
                if x_ptr>=1000:
                    pass
                else:
                    background.paste(blank_c,(x_ptr+advance,y_ptr))
                    x_ptr+=advance+1

print(f'Sucessfully generated {args.n_samples}')
