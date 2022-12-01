import numpy as np
import cv2 as cv
import os as os
from pathlib import Path
import sys as sys

# %% [markdown]
# Setup function for standalone use

# %%
def Setup():

    if (len(sys.argv) != 2):
        print("""Please run as follows:
            python puzzle.py <Image_Folder_Directory>
            
            Where the folder directory contains your imageset per puzzle.""")
        quit()

    source_path = Path(str(sys.argv[1]))
    
    global build_path
    build_path = Path("Build/")
    build_path.mkdir(exist_ok=True)
    return source_path

source_path = Setup()
print(source_path)
print("Running Puzzle")
# %%
# build_path = Path("Build/")
# build_path.mkdir(exist_ok=True)
# source_path = Path("Validation Test/map")     #This is source directory to change

#Setup Files for reading
puzzle_pieces = []
with os.scandir(str(source_path)) as entries:
    for entry in entries:
        puzzle_pieces.append(entry.name)

# %%
#Store answers
position_answers = []

# %% [markdown]
# Setup desired Markers here

# %%
# Set Marker Color Ranges 
# Note that CV uses BGR instead of RGB
blue_dot = [(200,0,0),(255,40,40),"blue"]
red_dot = [(0,0,200),(40,40,255),"red"]
markers = [blue_dot,red_dot]

# %%
def loader(image_filename:str):
    return cv.imread(str(source_path.joinpath(image_filename)))

# %% [markdown]
# The image searching mechanism

# %%
def solve_position(image_filename:str ) -> dict:
    # test_image = source_path.joinpath(image_filename)
    # loaded_image = cv.imread(str(test_image))
    loaded_image = loader(image_filename)

    #Pre=process image
    blurred_image = cv.medianBlur(loaded_image, 7)

    #Populate total markers in image to Dictionary
    circles = {}
    for lower_bound, upper_bound, color in markers:
        mask = cv.inRange(blurred_image,lower_bound, upper_bound)
        # cv.imshow('mask',mask)
        
        counts = cv.findContours(mask,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
        circles.update({color : len(counts[0])})
        # cv.destroyWindow('mask')
    
    # cv.destroyAllWindows()
        
    return circles

#Test function works as intended        
# assert( solve_position("Test Data/fumo/3Yy2JsTKtsLVG2RU.jpg") == {'blue':2, 'red':2})
    


# %% [markdown]
# Columns are Red, Rows are Blue
# 

# %%
#go through set of images
for image in puzzle_pieces:
    position = solve_position(image)
    solved_piece = position['red'], position['blue'], image
    position_answers.append(solved_piece)


# %%

#find the max row and column
row_size = 0
col_size = 0
for answer in position_answers:
    col_size = max(answer[0],col_size)
    row_size = max(answer[1],row_size)
    
#find shape of total 
single_shape = loader(puzzle_pieces[0]).shape
max_x = col_size * single_shape[0] 
max_y = row_size * single_shape[1] 

# %%
row_size, col_size

# %%
max_x, max_y

# %% [markdown]
# Sort pieces by coordinates and paste together

# %%
# Assemble picture

position_answers.sort(key= lambda elem: (elem[0],elem[1]))
horizontal_strip = []
row_section = []

for i in range(row_size):
    row_section.append(i)




count = 0
for i in position_answers:
    # print(i[2]," count is at", count)
    horizontal_strip.append(loader(i[2]))
    if (i[1] % col_size ==0):
        # print('--------')
        row_section[count] =  np.concatenate(horizontal_strip,axis=0)   #connect single images into horizontal strips
        count += 1
        horizontal_strip.clear()

solution = np.concatenate(row_section, axis=1) #connect horizontal strips of the images      


# %%
target_filename = f'Completed Puzzle_{str(max_y)}x{str(max_x)}.jpg'
target = str(build_path.joinpath(target_filename))

cv.imwrite(target, solution) 
print("Puzzle is now in Build/", target_filename)
#Done!


