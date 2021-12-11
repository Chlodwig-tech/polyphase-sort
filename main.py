import sys, os
import polyphase_sort
import read

def main():
    if os.name=='nt':
        source,destination='data\source.dat','data\destination.dat'
    else:
        source,destination='data/source.dat','data/destination.dat'

    debug,sort_ascending=False,True
    page_size=2048

    for i in range(len(sys.argv)):
        if sys.argv[i]=='-s':
            source=sys.argv[i+1]
            i+=1
        if sys.argv[i]=='-d':
            destination=sys.argv[i+1]
            i+=1
        if sys.argv[i]=='-r':
            read.read(source)
        if sys.argv[i]=='-debug':
            debug=True
        if sys.argv[i]=='-ps':
            page_size=int(sys.argv[i+1])
            i+=1
        if sys.argv[i]=='-sort':
            if sys.argv[i+1]=='f':
                sort_ascending=False
            if sys.argv[i+1]=='t':
                sort_ascending=True

    p=polyphase_sort.PolyphaseSort(page_size,source,destination,debug,sort_ascending)
    p.sort()

if __name__=='__main__':
    main()