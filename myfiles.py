import os
from PIL import Image
from PIL.ExifTags import TAGS
Image.MAX_IMAGE_PIXELS = None
printers = {'Сольвент':0,
            'Сублим':0,
            }
sol_templates = ('counter', 'popup', 'counter cat promo')
subl_templates = ('jc', 'textile', 'Press Wall Cat' )

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
                image_area_m = image_width*image_height
                print(f'{file_name[:30]}...: {image_width}m {image_height}m {image_area_m} m.sq.')

                for templ in sol_templates:
                    if templ in file_name.lower():
                        printers['Сольвент']+=image_area_m
                
                for templ in subl_templates:
                    if templ in file_name.lower():
                        printers['Сублим']+=image_area_m




            except OSError:
                print("cannot open", file_name)
        else:
            continue
print(f"Сольвентник - {printers['Сольвент']}, Сублимация-{printers['Сублим']}")



