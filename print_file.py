import sys

def get_value(record):
    l=[int(elem) for elem in record.split(',')]
    return l[0]+l[1]*l[-1]+l[2]*l[-1]**2+l[3]*l[-1]**3+l[4]*l[-1]**4

def get_pages(path,size):

    with open(path,'rb') as file:
        
        data=file.read(size).decode()
        m_data=''

        while data:
            
            l=data.split(';')

            if m_data!='':
                l[0]=m_data+l[0]
                m_data=''
            
            if data[-1]!=';':
                m_data=l[-1]
                del l[-1]

            if l:
                if l[-1]=='':
                    del l[-1]
                yield l
            
            data=file.read(size).decode()


l=[]
l3=[]

def print_file(path,size):
    gen=get_pages(path,size)
    for records in gen:
        for r in records:
            l.append(get_value(r))
            l3.append(r)

if __name__=='__main__':
    print_file(sys.argv[1],4096)
    l2=l[:]
    l2.sort()
    

    for i in range(len(l)):
        print(l3[i],l[i])

    if l==l2:
        print('xd',len(l))
    else:
        print('no')