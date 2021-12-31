import csv


def get_filename(name:str):
    if '.' in str(name):
        return name.split('.')[0]
    return name

def write_partial_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding="utf-8") as fo:
        writer = csv.writer(fo, delimiter=',')
        for row in data:
            writer.writerow(row)
            # pass
            
    return 

def split_csv_to(source_csv, num, result_csv):
    result_filename = get_filename(result_csv)
    with open(source_csv, 'r', encoding="utf-8") as fi:
        reader = csv.reader(fi, delimiter=',')
        csv_data = list(reader)
        num_csv_data = len(csv_data)
        num_processed = 0
        while num_processed < num_csv_data:  
            if (num_processed + num) < num_csv_data:
                partial_data = csv_data[:num]
            else:
                partial_data = csv_data[:(num_csv_data - num_processed)]

            num_csv_partial = len(partial_data)
            
            partial_filename = f'{result_filename}_({num_processed}-{num_processed + num_csv_partial - 1}).csv'
            write_partial_to_csv(partial_data, partial_filename)
            
            num_processed += num_csv_partial
            print(partial_filename)
        
        # print(len(csv_data))
    return 


split_csv_to(
    source_csv='fun_fact_on_Twitter.csv',
    num=100000,
    result_csv='fun_fact_on_Twitter.csv'
)