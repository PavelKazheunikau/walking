import os
from PIL import Image
from PIL.ExifTags import TAGS
Image.MAX_IMAGE_PIXELS = None
import json
def count_items(file_name:str):
    start_index  = file_name.find('.шт')
    if start_index>-1:
        count_num=[] 
        i=1
        while file_name[start_index-i].isdigit():
            count_num.append(file_name[start_index-i])
            i+=1
        return int(''.join(count_num[::-1]))
    else:
        return 1

    
printers = {'Сольвент':0,
            'Сублим':0,
            }
sol_templates = ('counter', 'popup', 'counter cat promo', 'баннер')
subl_templates = ('jc', 'textile', 'Press Wall Cat' )
direct_templates= ('сетка')

for folder, subfolders, filenames in os.walk('c:\\work\\my_projects\\walking\\'):
    for file_name in filenames:
        extention = os.path.splitext(file_name)[1]        
        if extention in ('.jpg', '.tiff', '.tif'):
            path = os.path.join(folder, file_name)         
            file_info = {}            
            try:
                with Image.open(path) as myfile:
                    exif_data = myfile.getexif()
                    if exif_data:
                        for tag, value in exif_data.items():                            
                            if TAGS[tag] == 'XResolution':
                                file_info['XRes']=value
                                break                                               
                    elif myfile.info:
                        file_info['XRes'] = myfile.info.get('dpi'[0], 72)
                    else:
                        print(f'file {file_name[:15]}... не имеет информации')
                        continue
                
                image_width = myfile.width/file_info['XRes']*2.54/100
                image_height = myfile.height/file_info['XRes']*2.54/100
                count_=count_items(file_name.lower())          
                image_area_m = image_width*image_height*count_
        
                for templ in sol_templates:
                    if templ in file_name.lower():
                        printers['Сольвент']+=image_area_m
                        print(f'Сольвент - {file_name:.20}...: Шир-{image_width:10.4f}m Выс-{image_height:10.4f}m кол-во-{count_:4d} {image_area_m:10.4f} m.sq.')
                        break
                    else:
                        printers['Сублим']+=image_area_m
                        print(f'Сублим. - {file_name:.20}...: Шир-{image_width:10.4f}m Выс-{image_height:10.4f}m кол-во-{count_:4d} {image_area_m:10.4f} m.sq.')
                        break



            except OSError:
                print("cannot open", file_name)
        else:
            continue
print(f"Сольвентник - {printers['Сольвент']}, Сублимация-{printers['Сублим']}")



