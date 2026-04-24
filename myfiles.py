import os, csv, sys
from PIL import Image
from PIL.ExifTags import TAGS
import openpyxl
Image.MAX_IMAGE_PIXELS = None


def count_items(file_name:str): # defines count of print copies

    start_index  = file_name.find('(д)')
    if start_index > -1:
        while not file_name[start_index-1].isdigit():
            newfilename=file_name[:start_index-1]+file_name[start_index:]    #removing simbols between nums and шт.
            start_index-=1   #go from right to left
        count_num=[]  #number of copies
        i=1
        while file_name[start_index-i].isdigit():
            count_num.append(file_name[start_index-i])  #gather digits of num in reverse
            i+=1
        return int(''.join(count_num[::-1]))    #unreverse
    else:
        return 1

def job_area(file_path:str):
    file_info = {}
    try:
        with Image.open(file_path) as myfile:
            exif_data = myfile.getexif()
            if exif_data:
                file_info['XRes'] = myfile.info.get('dpi', 72)[0]
            else:
                print(f'file {file_name[:60]}... не имеет информации')
                return 0


        image_width = myfile.width/file_info['XRes']*2.54/100   #meters
        image_height = myfile.height/file_info['XRes']*2.54/100
        count_= count_items(file_path.lower())                  # copies
        image_area_m = image_width*image_height*count_          # area of all copies(whole order)

    except OSError:
                print("cannot open", file_name)
    return  image_area_m


search_templates={
    'p-SOL':
        {'m-SCL':['Самоклейка',0],
        'm-BNb':['Баннер Блекаут',0],
        'm-BN':['Баннер стандартный',0],
        'm-PP':['Полипропилен',0]
        },
    'p-PRM':
        {'m-ISH':['Искусственный шёлк',0],
        'm-FS115':['Флажная сетка 115',0],
        'm-FS90':['Флажная сетка 90',0],
        },
    'p-SUB': {
        'm-ATL':['Атлас',0],
        'm-BFL':['Бифлекс',0],
        'm-GBD':['Габардин',0],
        'm-DNS':['Двунитка суровая',0],
        'm-DKT':['Декатекс',0],
        'm-DSP':['Дюспо',0],
        'm-ILN':['Искусственный лён',0],
        'm-LS':['Ложная сетка',0],
        'm-MBL':['Микробэклайт',0],
        'm-MGT':['Моготекс',0],
        'm-ATL':['Атлас',0],
        'm-WSH':['Мокрый шелк',0],
        'm-NIK':['Ника',0],
        'm-OX210':['Оксфорд 210',0],
        'm-OX600':['Оксфорд 600',0],
        'm-PMF':['Прима микрофибра',0],
        'm-SAT':['Сатен',0],
        'm-SPL':['Спейслайт',0],
        'm-HKN':['Хоккейная сетка',0],
        'm-CHF':['Шифон',0],
        'm-ATLS':['Атлас на сетке',0],
        'm-SHR':['Шармус',0],
        'm-MFL110':['Микрофибра "Лето" 110 гр.',0],
        'm-DSH':['Дешайн',0],
        'm-BKO':['Блэкаут',0],
        'm-FLS':['Флис',0],
        'm-FTR':['Футер',0],
        'm-TKZ':['Ткань заказчика',0],
        'm-TTB':['Бумага термотрансферная',0]
        }
    }

#to do: finish dictionary"!!!


other_files=[]
dict_to_csv=[]
printed_files = []
for folder, subfolders, filenames in os.walk('c:/temp/2026.04.13/'):
    for file_name in filenames:
        ext = os.path.splitext(file_name)[1]  # extention
        main_name = os.path.splitext(file_name)[0]
          # filename
        if ext in ('.tiff', '.tif'):
                path = os.path.join(folder, file_name) # full name
                printed_files.append(path)
        else:
                path = os.path.join(folder, file_name)
                other_files.append(path)# files except printed (orders, preview)

#to do: обход каталога и сохранение списка печатных файлов"!!!
#to do: формир словаря с заказами и площ печати по материалам и видам печати"
#to do: сформировать список с работами и площадью "!!!
#to do: посчитать сумму печати по матералам и категориям"

#to do: площадь заказа в отд функцию"!!!
#to do: вывод на экран словаря с данными"
#to do: запись словаря в файл"pass
areas = []
for job in printed_files:
     areas.append(job_area(job))

all_jobs = list(zip(map(os.path.basename, printed_files), areas))

find_flag = False                                       # to suspend  more search
row_dict=[]
for job, area in  all_jobs:
    for print_type in search_templates:
        if print_type in job:
            for material in search_templates[print_type]:
                if material in job:
                    dict_to_csv.append([print_type,material, job, area])  # data to write to csv
                    print(job, '- запись')
                    break
            else:
                print(job,'материал указан неверно')
            break
    else:
        print(job, 'неизв. тип печати')

print(len(dict_to_csv))

# for print_type in search_templates:
                            # every type of print
#         for template in search_templates[printer_type][0]:  # list of search words
#             if template in file_name.lower():
#                 search_templates[printer_type][1]+=image_area_m #  add area to specific printer
#                 formatted_output = (
#                     f'{printer_type:<12} - {template:_<15}-{file_name:>.25}...:   '
#                     f'Ширина -{image_width:>5.2f} м   '
#                     f'Высота -{image_height:>5.2f} м   '
#                     f'Кол-во -{count_:>3d} шт.   '
#                     f'Площадь -{image_area_m:>6.2f} м.кв.'
#                 )
#                 print(formatted_output)
#                 dict_to_csv.append([printer_type,template, file_name, image_width, image_height, count_, image_area_m])
#                 find_flag = True                            # file is calculated
#                 break
#         else:
#             continue
#         if find_flag:                                       #go to next file is this one is calculated. Terminate outer for
#             break
# else:                                                   #name doesn't matches any key word
#     print(f'Непонятка! Добавлено к сублимации - {file_name} - {image_area_m:>6.2f}')
#     search_templates['solvent'][1]+=image_area_m
#     dict_to_csv.append(['solvent','непонятка', file_name, image_width, image_height, count_, image_area_m])
#         # file name doesn't fit any search word


#
# for key,value in search_templates.items():
#     print(f'{key} - {value[1]:.2f}', end='\t')
# print()
# print(f'Total - {sum(value[1] for value in search_templates.values()):.2f} в {printed_files_num}  печатных файлах')
# print(f'Запись в файл')
# with open('month_data.csv', mode='w', newline='') as csv_file:
#     writer=csv.writer(csv_file)
#     writer.writerows(dict_to_csv)
# input('Нажми любую клавишу')
