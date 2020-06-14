#Generates data for text detection.

import numpy as np
import argparse
from PIL import Image,ImageDraw,ImageFilter
import random
import os
from xml.etree.ElementTree import Element
from xml_utils import addObject,write_as_file

#Variables declaration.
file_count=0

global x_ptr,y_ptr,advance,back_copy
x_ptr=0
y_ptr=10
word_lengths=[2,3,4,5,6]
coor_list=[]

upper_char_list=[]
lower_char_list=[]
advance=25
image_sizes=[15,20,25,30,35,40,45,50]
background_arr=[]

def resize_images(arr,new_size):
    new_arr=[img.resize((new_size,new_size)) for img in arr]
    return new_arr

#Parsing stuff.

parser=argparse.ArgumentParser()
parser.add_argument('--n_samples',type=int,help='No of images to generate.',default=1)
parser.add_argument('--char_type',type=int,help='1 for all letters are capital 2 for all small and 3 for mix and 4 for capital at start.',
                    default=1)
parser.add_argument('--same_sizes',type=int,help='1 for same_size 2 for different_sizes')
args=parser.parse_args()


#Loading images.
for filename in os.listdir('./background/'):
    background_arr.append(Image.open('./background/'+filename))


blank=Image.open('./objects/blank.jpg')

upper_letters_name=os.listdir('./objects/upper/')
for filename in upper_letters_name:
    upper_char_list.append(Image.open('./objects/upper/'+filename))

lower_letters_name=os.listdir('./objects/lower/')
for filename in lower_letters_name:
    lower_char_list.append(Image.open('./objects/lower/'+filename))


both_char_list=[]
both_char_list.extend(upper_char_list)
both_char_list.extend(lower_char_list)

both_letters_name=[]
both_letters_name.extend(upper_letters_name)
both_letters_name.extend(lower_letters_name)




#Placing char images in random places and recording their annotations in xml file.

for _ in range(args.n_samples):
    top=Element('Annotations')

    back_copy=random.choice(background_arr).copy()
    upper_char_list_c=upper_char_list.copy()
    lower_char_list_c=lower_char_list.copy()
    both_char_list_c=both_char_list.copy()
    blank_c=blank.copy()

    #In case we want to have chars of various aspect ratios.
    if args.same_sizes==2:
        new_size=random.choice(image_sizes)
        upper_char_list_c=resize_images(upper_char_list_c,new_size)
        lower_char_list_c=resize_images(lower_char_list_c,new_size)
        both_char_list_c=resize_images(both_char_list_c,new_size)
        blank_c=blank_c.resize((new_size,new_size))

    while True:
        if x_ptr>=800:
            x_ptr=0
            y_ptr+=advance*4
        elif y_ptr>=800:
            if args.char_type==1:
                back_copy.save(f'./generated_data/Images/{str(file_count)}_1.jpg')
                write_as_file(f'./generated_data/Annotations/{str(file_count)}_1',top)
            elif args.char_type==2:
                back_copy.save(f'./generated_data/Images/{str(file_count)}_2.jpg')
                write_as_file(f'./generated_data/Annotations/{str(file_count)}_2',top)
            elif args.char_type==3:
                back_copy.save(f'./generated_data/Images/{str(file_count)}_3.jpg')
                write_as_file(f'./generated_data/Annotations/{str(file_count)}_3',top)
            else:
                back_copy.save(f'./generated_data/Images/{str(file_count)}_4.jpg')
                write_as_file(f'./generated_data/Annotations/{str(file_count)}_4',top)
            file_count+=1
            x_ptr=0
            y_ptr=10
            break

        else:
            word_len=random.choice(word_lengths)
            x_ptr_s=x_ptr
            y_ptr_s=y_ptr
            for j in range(word_len):
                if x_ptr>=800:
                    pass
                else:
                    if args.char_type==1:
                        idx=np.random.randint(0,len(upper_char_list_c))
                        back_copy.paste(upper_char_list_c[idx],(x_ptr+advance,y_ptr))
                        label=upper_letters_name[idx].split('.')[0].split('_')[0]

                    elif args.char_type==2:
                        idx=np.random.randint(0,len(lower_char_list_c))
                        back_copy.paste(lower_char_list_c[idx],(x_ptr+advance,y_ptr))
                        label=lower_letters_name[idx].split('.')[0].split('_')[0]


                    elif args.char_type==4:
                        if x_ptr==0:
                            idx=np.random.randint(0,len(upper_char_list_c))
                            back_copy.paste(upper_char_list_c[idx],(x_ptr+advance,y_ptr))
                            label=upper_letters_name[idx].split('.')[0].split('_')[0]

                        else:
                            idx=np.random.randint(0,len(lower_char_list_c))
                            back_copy.paste(lower_char_list_c[idx],(x_ptr+advance,y_ptr))
                            label=lower_letters_name[idx].split('.')[0].split('_')[0]

                    elif args.char_type==3:
                        idx=np.random.randint(0,len(both_char_list_c))
                        back_copy.paste(both_char_list_c[idx],(x_ptr+advance,y_ptr))
                        label=both_letters_name[idx].split(".")[0].split('_')[0]

                    else:
                        pass
                    x_ptr+=advance+1
            
            top=addObject(top,label,x_ptr_s,y_ptr_s,x_ptr_s+(advance*word_len),y_ptr_s+advance)



            for i in range(3):
                if x_ptr>=800:
                    pass
                else:
                    back_copy.paste(blank_c,(x_ptr+advance,y_ptr))
                    x_ptr+=advance+1

print(f'Sucessfully generated {args.n_samples}')
