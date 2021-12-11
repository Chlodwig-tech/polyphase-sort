import generate_records
import polyphase_sort

import matplotlib.pyplot as plt
import math

def test():
    x,y=[],[]
    teoritical_values=[]
    
    source,destination='data/source.dat','data/destination.dat'
    l=[100,500,1000,10000,100000]

    p=polyphase_sort.PolyphaseSort(1024,source,destination)

    for number_of_records in l:
        print(number_of_records)
        generate_records.generate_records(source,number_of_records)
        p.sort()
        x.append(number_of_records)
        y.append(p.number_of_reads+p.number_of_writes)
        teoritical_values.append(2*number_of_records*(1.04*math.log(number_of_records/2,2))/1024*13)
        print('-----------------------------')
    
    plt.title('Liczba operacji dyskowych zależnie od N')
    plt.plot(x,y,label='Liczba operacji dyskowych')
    plt.plot(x,teoritical_values,label='Teorytyczna liczba operacji dyskowych')
    plt.xlabel('N')
    plt.ylabel('Liczba operacji dyskowych')
    plt.legend()
    plt.show()

    print(x)
    print(y)
    print(teoritical_values)

if __name__=='__main__':
    test()