import numpy as np
import matplotlib.pyplot as plt
from PIL import Image,ImageDraw,ImageFont
import cv2
import argparse
import string
import random
import os
from xml.etree.ElementTree import Element
from xml_utils import addObject,write_as_file
from tqdm import tqdm

parser=argparse.ArgumentParser()
parser.add_argument('--n_samples',type=int,help='No of samples to generate.')
parser.add_argument('--char_type',type=int,help='1 for all small 2 for all caps and 3 for caps char in starting')

args=parser.parse_args()

#Variable declaration.
global x_ptr,y_ptr,file_count
x_ptr,y_ptr=(0,0)
fontlist=[]
file_count=0




back_locs=os.listdir('./background/')
background_imgs=[]

for filename in back_locs:
	background_imgs.append(Image.open('./background/'+filename))

fonts=os.listdir('./fonts/')
for ftname in fonts:
	fontlist.append('./fonts/'+ftname)




for _ in tqdm(range(args.n_samples)):
	top=Element('Annotations')
	background=random.choice(background_imgs).copy()
	draw=ImageDraw.Draw(background)
	font=ImageFont.truetype(random.choice(fontlist),size=random.choice([4,6,8,10,12,16]))
	bounding_boxes=[]
	while True:
		if args.char_type==1:
			chars=list(string.ascii_lowercase)
			random.shuffle(chars)
			word=''.join(chars[:random.choice([2,3,4,5,6,7,8,9,10,11,12,12])])
		elif args.char_type==2:
			chars=list(string.ascii_uppercase)
			random.shuffle(chars)
			word=''.join(chars[:random.choice([2,3,4,5,6,7,8,9,10,11,12,12])])
		else:
			upper_chars=list(string.upper_case)
			lower_chars=list(string.lower_case)
			word=''.join(upper_chars[random.choice(upper_chars)]).join(lower_chars[:random.choice([1,2,3,4,5,6,7,8,9,10,11])])


		
		if x_ptr>=np.array(background).shape[1]:
			x_ptr=0
			y_ptr+=20
		elif y_ptr>=np.array(background).shape[0]:
			x_ptr=0
			y_ptr=0
			background.save(f'./generated_data/Images/{file_count}.jpg')
			write_as_file(f'./generated_data/Annotations/{file_count}',top)
			break
		else:
			draw.text((x_ptr,y_ptr),text=word,font=font,fill='rgb(0,0,0)')
			top=addObject(top,'text',x_ptr,y_ptr,x_ptr+font.getsize(word)[0],y_ptr+font.getsize(word)[1])
		x_ptr+=font.getsize(word)[0]+5
	file_count+=1


print("Done")















