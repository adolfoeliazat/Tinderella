# modules I wrote
from Pipeline_CommonFunctions import clean_file_lst
import os


item_dict = {}
new_lst = []
full_path = '/Users/heymanhn/Virginia/Zipfian/Capstone_Project/Web_App/data/Image_20Percent'
clean_stand_img_directory_lst = clean_file_lst(os.listdir(full_path), jpg=False)
count = 0
for i, subdir in enumerate(clean_stand_img_directory_lst):
	subdir_path = os.path.join(full_path, subdir)
	clean_img_lst = clean_file_lst(os.listdir(subdir_path), jpg=True)
	for j, img_file in enumerate(clean_img_lst):
		new_lst.append(img_file)
		item_dict[img_file] = count
		count +=1

print item_dict['barneys_158585078.jpg']
print item_dict['saks_0471952635914.jpg']
print len(item_dict)

print len(new_lst)