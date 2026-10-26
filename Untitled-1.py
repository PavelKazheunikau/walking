def count_d(filename:str):

    start_index = filename.find('шт')
    i=0
    if start_index>-1:
        while not filename[start_index-i-1].isdigit():
            i+=1
        num_end = start_index-i

        while filename[start_index-i-1].isdigit():
            i+=1
        num_start = start_index-i
        return int(filename[num_start:num_end])
    else:
        return 1

print (count_d('печать_10000   шт (дубль)') )
