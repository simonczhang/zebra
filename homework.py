import csv
from pprint import pprint

def null_check(v):
    if v == '':
        return False
    
    return True

def file_checker(file, output_schema):
    '''This function checks to make sure the csv contains all necessary fields to add to output'''
    input_fields = [] 
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        #check to see if there's anything in first row of the csv
        try: 
            input_fields = next(csv_reader) 
        except StopIteration:
            return {'status': False, 'msg':'Input file is blank'}
        
        #check which columns in input are also in output
        output_fields = set(output_schema)
        contained_fields = set(input_fields).intersection(output_fields) 
        
        if contained_fields != output_fields:
               return {'status':False, 'msg':f'Input file is missing required column(s): {output_fields.difference(contained_fields)}'}
        else:
            return {'status':True, 'msg':'Input file valid'}
        
def strip_quotes(s):
    '''This function strips starting and ending quotes. I assume that all quotes should be stripped in this exercise'''
    if s == '':
        return ''

    if s[0] == s[-1] == '"':
        return strip_quotes(s[1:-1])
    elif s[0] == s[-1] == "'":
        return strip_quotes(s[1:-1])
    else:
        return s
        
def clean_field(field, value):
    '''This function performs all the checks for each value based on the output schema requirements'''

    try:
        assert isinstance(value, str)
        assert isinstance(field, str)
    except AssertionError:
        raise BaseException('Field and Value inputs must both be type string')
    
    if field == 'Provider Name':
        if not null_check(value):
            print(f'Found null value in field: {field}')
            return None
        
        return strip_quotes(value)
        
    elif field == 'CampaignID':
        if not null_check(value):
            print(f'Found null value in field: {field}')
            return None
        
        return strip_quotes(value)
        
    elif field == 'Cost Per Ad Click':
        if not null_check(value):
            print(f'Found null value in field: {field}')
            return None
        
        #check if value can be converted to float
        stripped_value = strip_quotes(value).replace(',', '')
        
        try:
            stripped_value = float(stripped_value)
        except ValueError:
            print(f'Invalid value: {value} for field: {field}')
            return None

        if stripped_value < 0: #not sure how to handle negative numbers. Will allow it in this exercise
            print(f'Float is negative: {stripped_value}.\nAre you sure this is a valid input?')
        
        return stripped_value
        
    elif field == 'Redirect Link':
        if not null_check(value):
            print(f'Found null value in field: {field}')
            return None
        
        return strip_quotes(value)
    
    elif field == 'Phone Number':
        if len(value) == 0:
            return ''
        
        return strip_quotes(value)
    
    elif field == 'Address':
        if not null_check(value):
            print(f'Found null value in field: {field}')
            return None
        
        return strip_quotes(value)
        
    elif field == 'Zipcode':
        if not null_check(value):
            print(f'Found null value in field: {field}')
            return None
        
        return strip_quotes(value)
        
    else:
        raise BaseException(f'Passed field: {field}, doesn\'t match a field in the output schema or new field logic hasn\'t yet been added to function')
    
    
def process_file(file, output_p, output_schema):
    with open(file, 'r') as csv_file:
        print(f'Beginning Process for: {file}')
        csv_reader = csv.DictReader(csv_file)

        with open(output_p, 'a', newline='') as output_file:
            csv_writer = csv.writer(output_file, lineterminator="\n")
            #we loop through the file
            added_rows = 0
            for i, row in enumerate(csv_reader):
                sorted_row = []
                for field in output_schema:
                    #and perform some checks on the values of each row
                    cleaned_field = clean_field(field, row[field])
                    if cleaned_field == None:
                        break
                    else:
                        sorted_row.append(cleaned_field)

                #then write the row to the output file  
                if len(sorted_row) == len(output_schema):
                    csv_writer.writerow(sorted_row)
                    added_rows += 1
                else:
                    print(f'At least one error while cleaning csv.\nFailed to import field: {field}, row: {i}.')

        print(f'Finished adding rows to: {file}\n')
        
        return added_rows
        
def process_csvs(file_list, output_path, output_schema):
    #create the output file and add the fields row
    with open(output_path, 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file, lineterminator="\n")
        csv_writer.writerow(output_schema)

    imported_files = 0
    failures = {} #keep track of all input files that failed the checker so we can reach back to partners about issue
    for file in file_list:
        r = file_checker(file, output_schema)
        if r['status']:
            process_file(file, output_path, output_schema)
            imported_files += 1
        else:
            #if the input file doesn't pass the checker then we move to the next file
    #         print(f"{file}: {r['msg']}")
            failures[file] = r['msg']

    print('All Imports Complete\n')

    #print all failures
    print('IMPORT FILES ERROR LOG:\n')
    for k, v in failures.items():
        print(f'{k}: {v}\n')
        
    return imported_files

if __name__ == '__main__':
    f = [

             'Homework - Auto Insurance.csv', 
             'Homework - Home Insurance.csv'

    ]
    
    o = 'output.csv'

    schema = ['Provider Name', 
                'CampaignID', 
                'Cost Per Ad Click', 
                'Redirect Link', 
                'Phone Number', 
                'Address', 
                'Zipcode']

    process_csvs(f, o, schema)
    #print the output file to 
    print('FINAL OUTPUT FILE: TOP 15 ROWS\n')
    with open(o, 'r') as f:
        csv_r = csv.reader(f)

        for i, line in enumerate(csv_r):
            if i > 15:
                break
            else:
                print(line)


        
