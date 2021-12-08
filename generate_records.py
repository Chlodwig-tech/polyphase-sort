from random import randint
import sys

def generate_records(path,number_of_records):
    with open(path,'wb') as file:
        data=''
        for _ in range(number_of_records):
            for _ in range(5):
                data+=f'{randint(1,10)},'
            data+=f'{randint(1,10)};'
        file.write(data.encode())


if __name__=='__main__':
    generate_records(sys.argv[1],int(sys.argv[2]))