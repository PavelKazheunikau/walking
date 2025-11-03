import os
from PIL import Image
from PIL.ExifTags import TAGS
import openpyxl
Image.MAX_IMAGE_PIXELS = None
def count_items(file_name:str): # defines count of print copies
    start_index  = file_name.find('шт')
    if start_index > -1:
        count_num=[] 
        i=1
        while file_name[start_index-i].isdigit():
            count_num.append(file_name[start_index-i])
            i+=1
        return int(''.join(count_num[::-1]))
    else:
        return 1

search_templates={
    'solvent':
    [('с_кл','counter cat promo', 'counter', 'popup', 'баннер','промо', 'скл'),0],
    'sublimation':
    [('jc', 'textile', 'press wall cat', 'габардин', 'мокрый шелк','сатен','моготекс', 'атлас', 'бумага' ),0],
    'direct':
    [('сетка','прямая'),0]
    }

dict_to_csv=[]
for folder, subfolders, filenames in os.walk('.'):
    for file_name in filenames:
        extention = os.path.splitext(file_name)[1]  # extention      
        if extention in ('.jpg', '.tiff', '.tif'):
            path = os.path.join(folder, file_name)   # full name      
            file_info = {}            
            try:
                with Image.open(path) as myfile:
                    exif_data = myfile.getexif()
                    if exif_data:
                        for tag, value in exif_data.items():                            
                            if TAGS[tag] == 'XResolution':
                                file_info['XRes']=value # get dpi
                                break                                               
                    elif myfile.info:
                        file_info['XRes'] = myfile.info.get('dpi'[0], 72)
                    else:
                        print(f'file {file_name[:15]}... не имеет информации')
                        continue
                
                image_width = myfile.width/file_info['XRes']*2.54/100   #meters
                image_height = myfile.height/file_info['XRes']*2.54/100
                count_= count_items(file_name.lower())                  # copies
                image_area_m = image_width*image_height*count_          # area of all copies(whole order)
                find_flag = False                                       # to suspend  more search
                row_dict=[]                                             # data to write to csv
                for printer_type in search_templates:                   # every type of print
                    for template in search_templates[printer_type][0]:  # list of search words            
                        if template in file_name.lower():
                            search_templates[printer_type][1]+=image_area_m #  add area to specific printer
                            formatted_output = (
                                f'{printer_type:<12} - {template:_<15}-{file_name:>.25}...:   '
                                f'Ширина -{image_width:>5.2f} м   '
                                f'Высота -{image_height:>5.2f} м   '
                                f'Кол-во -{count_:>3d} шт.   '
                                f'Площадь -{image_area_m:>6.2f} м.кв.'
                            )                                            
                            print(formatted_output)
                            row_dict.append[printer_type,template, file_name, image_width, image_height, count_, image_area_m]
                            find_flag = True                            # file is calculated
                            break
                    if find_flag:                                       #go to next file is this one is calculated
                        break
                else:
                    print('-Непонятка!'+file_name)                       # file name doesn't fit any search word


            except OSError:
                print("cannot open", file_name)
        else:
            continue
    dict_to_csv.append(row_dict)
for key,value in search_templates.items():
    print(f'{key} - {value[1]:.2f}', end='\t')
print()
# print(f"Сольвентник - {['Сольвент']}, Сублимация-{printers['Сублим']}")
print(f'Total - {sum(value[1] for value in search_templates.values()):.2f}')

input()