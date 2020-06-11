# Synthetic-data-generator-for-OCR.
This is a program which generates the images containing english characters arranged
in a lined fashion just like book.It generates the images with annotations in Pascal VOC format.

To generate new data run `python generate_data.py --n_samples num_samples`

## Args

* --n_samples: No of images to generate
* --char_type: whether to generate with all characters in upper case,lower case,both or starting letter capital only.1 for all letters are capital 2 for all small and 3 for mix and 4 for capital at start
* --same_sizes: wether all images contain same sizes characters.
