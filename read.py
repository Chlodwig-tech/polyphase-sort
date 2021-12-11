def read(path):
    with open(path,'ab') as file:
        print('Enter the record (each of the 6 words after a comma) otherwise `stop`')
        print('For example: 5,2,4,5,3,2;')
        print('stop')
        l=''
        while True:
            record=input()
            if record=='stop':
                break
            else:
                l+=record
        file.write(l.encode())

if __name__=='__main__':
    read('data/source.dat')