import csv
from tqdm import tqdm

def append_csv(source, new_data):
    with open(source, 'r', encoding='utf-8') as source_file_read, \
        open(new_data, 'r', encoding='utf-8') as new_file:
        source_file_reader = csv.reader(source_file_read)
        new_file_reader = csv.reader(new_file)
        
        source_file_reader_as_list = list(source_file_reader)[2:]
        new_file_reader_as_list =  list(new_file_reader)
        joined_list = new_file_reader_as_list + source_file_reader_as_list
        
        print(f'Writing new version of {source}!')
        with open(source, 'w', encoding='utf-8', newline='') as source_file_write:
            source_file_writer = csv.writer(source_file_write, delimiter=',')
            for row in tqdm(joined_list):
                source_file_writer.writerow(row)
        
        print('Summary: ', len(source_file_reader_as_list) + 2, ' rows, now became ', len(joined_list), 'rows') 
            
    return 


def get_filename(name:str):
    if '.' in str(name):
        return name.split('.')[0]
    return name

def write_partial_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding="utf-8") as fo:
        writer = csv.writer(fo, delimiter=',')
        for row in tqdm(data):
            writer.writerow(row)
            # pass
            
    return 

def split_csv_to(source_csv, num, result_csv):
    result_filename = get_filename(result_csv)
    with open(source_csv, 'r', encoding="utf-8") as fi:
        reader = csv.reader(fi, delimiter=',')
        print('Reading data: ')
        csv_data = list(tqdm(reader))[1:]
        num_csv_data = len(csv_data)
        num_processed = 0
        while num_processed < num_csv_data:
            if (num_processed + num) < num_csv_data:
                partial_data = csv_data[:num]
            else:
                partial_data = csv_data[num_processed:]

            num_csv_partial = len(partial_data)
            
            partial_filename = f'{result_filename}_({num_processed + 1}-{num_processed + num_csv_partial}).csv'
            print('Now writing: ', partial_filename)
            write_partial_to_csv(partial_data, partial_filename)
            
            num_processed += num_csv_partial
        
        # print(len(csv_data))
    return 