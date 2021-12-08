import sys
import os

class PolyphaseSort:

    def __init__(self,page_size,source,sort_ascending=True):
        self.number_of_reads=0
        self.number_of_writes=0
        self.number_of_phases=0
        self.fib_list=[1,1]
        self.end=0

        self.page_generators={}
        self.records_generators={}
        self.tapes={}
        
        self.page_size=page_size
        self.source=source
        self.stop=False
        self.sort_ascending=sort_ascending

        self.page_generators[source]=None

        for i in range(3):
            self.tapes[f'tapes/tape{i+1}.dat']=''
            self.page_generators[f'tapes/tape{i+1}.dat']=None
            self.records_generators[f'tapes/tape{i+1}.dat']=None

    def get_10_more_fib_numbers(self):
        for _ in range(10):
            self.fib_list.append(self.fib_list[-1]+self.fib_list[-2])

    def get_pages(self,path,page_size):
        with open(path,'rb') as file:
            data=file.read(page_size).decode()
            self.number_of_reads+=1
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
                data=file.read(page_size).decode()
                self.number_of_reads+=1
            
    def get_records(self,path):
        try:
            l=next(self.page_generators[path])
            for element in l:
                yield element
        except:
            self.stop=True

    def get_record(self,path):
        try:
            record=next(self.records_generators[path])
            return record
        except:
            self.records_generators[path]=self.get_records(path)
            if self.stop:
                self.stop=False
                return None
            return self.get_record(path)

    def init_generator(self,path):
        if not self.page_generators[path]:
            self.page_generators[path]=self.get_pages(path,self.page_size)

    def save_record(self,path,record):
        self.tapes[path]+=record+';'
        if sys.getsizeof(self.tapes[path])>=self.page_size:
            with open(path,'ab') as file:
                file.write(self.tapes[path].encode())
                self.number_of_writes+=1
                self.tapes[path]=''

    def save(self,path):
        if self.tapes[path]!='':
            with open(path,'ab') as file:
                file.write(self.tapes[path].encode())
                self.number_of_writes+=1
                self.tapes[path]=''

    @staticmethod
    def get_value(record):
        l=[int(elem) for elem in record.split(',')]
        return l[0]+l[1]*l[-1]+l[2]*l[-1]**2+l[3]*l[-1]**3+l[4]*l[-1]**4

    def cmp_values(self,v1,v2):
        if not v2:
            return False
        if self.sort_ascending:
            return v1<v2
        return v1>v2

    def distribution(self):
        open('tapes/tape1.dat','w').close()
        open('tapes/tape2.dat','w').close() 

        self.init_generator(self.source)

        t=True
        len1,len2=0,0
        pv=None
        prun1,prun2=None,None
        index=0
        c1,c2=False,False

        while True:
            record=self.get_record(self.source)
            if not record:
                break
            value=self.get_value(record)
            if self.cmp_values(value,pv):
                if t:
                    len1+=1
                    prun1=pv
                    if len1>=self.fib_list[index]:
                        index+=1
                        if index>=len(self.fib_list):
                            self.get_10_more_fib_numbers()
                        t=not t
                        c1=True
                else:
                    len2+=1
                    prun2=pv
                    if len2>=self.fib_list[index]:
                        index+=1
                        if index>=len(self.fib_list):
                            self.get_10_more_fib_numbers()
                        t=not t
                        c2=True
                
            pv=value
            if t and c1:
                if not self.cmp_values(value,prun1):
                    len1-=1
                c1=False
            if not t and c2:
                if not self.cmp_values(value,prun2):
                    len2-=1
                c2=False

            self.save_record(f'tapes/tape{1 if t else 2}.dat',record)

        self.save('tapes/tape1.dat')
        self.save('tapes/tape2.dat')

        if t:
            len1+=1
        else:
            len2+=1

        return len1,len2,index

    def first_merge(self,path,n):
        if n>0:
            open('tapes/tape3.dat','w').close()
            self.init_generator(path)
            success=0
            pv=None
            while True:
                record=self.get_record(path)
                if record:
                    v=self.get_value(record)
                    if self.cmp_values(v,pv):
                        success+=1
                        if success==n:
                            break
                    self.save_record('tapes/tape3.dat',record)
                    pv=v
                else:
                    break
            return record
        return None

    def merge(self,t1,t2,record1,record2,exx=False):
        print('n: ',self.number_of_phases)
        self.number_of_phases+=1
        
        
        r1_tape,r2_tape=f'tapes/tape{t1}.dat',f'tapes/tape{t2}.dat'
        w1=1 if (t1==2 and t2==3) or (t1==3 and t2==2) else 2 if (t1==1 and t2==3) or (t1==3 and t2==1) else 3
        w_tape=f'tapes/tape{w1}.dat'

        if not exx:
            if not record1 and not record2:
                self.number_of_phases-=1
                if os.stat(r1_tape).st_size==os.stat(self.source).st_size:
                    print(r1_tape)
                else:
                    print(r2_tape)
                return

        self.init_generator(r1_tape)
        self.init_generator(r2_tape)

        pv1,pv2=None,None
        r1,r2=True,True
        x1,x2=False,False

        nnn=0

        if record1:
            r1=False
            v1=self.get_value(record1)
            pv1=v1
        if record2:
            r2=False
            v2=self.get_value(record2)
            pv2=v2

        while True:
            if r1:
                record1=self.get_record(r1_tape)
                if record1:
                    v1=self.get_value(record1)
                    r1=False
                    if self.cmp_values(v1,pv1):
                        nnn+=1
                        while True:
                            if record2:
                                if self.cmp_values(v2,pv2):
                                    pv2=v2
                                    break
                                self.save_record(w_tape,record2)
                                pv2=v2
                                record2=self.get_record(r2_tape)
                                if not record2:
                                    x1=True
                                    break
                                v2=self.get_value(record2)
                            else:
                                break
                    if x1:
                        break
                    pv1=v1
                else:
                    break
            if r2:
                record2=self.get_record(r2_tape)
                if record2:
                    v2=self.get_value(record2)
                    r2=False
                    if self.cmp_values(v2,pv2):
                        nnn+=1
                        while True:
                            if record1:
                                if self.cmp_values(v1,pv1):
                                    pv1=v1
                                    break
                                self.save_record(w_tape,record1)
                                pv1=v1
                                record1=self.get_record(r1_tape)
                                if not record1:
                                    x2=True
                                    break
                                v1=self.get_value(record1)
                            else:
                                break
                    if x2:
                        break
                    pv2=v2
                else:
                    break

            if self.cmp_values(v1,v2):
                self.save_record(w_tape,record1)
                r1=True
            else:
                self.save_record(w_tape,record2)
                r2=True
        
        
        #print(f'nnn: {nnn}')

        if record1:
            while True:
                if record1:
                    if self.cmp_values(v1,pv1):
                        pv1=v1
                        break
                    self.save_record(w_tape,record1)
                    pv1=v1
                    record1=self.get_record(r1_tape)
                    if not record1:
                        break
                    v1=self.get_value(record1)
                else:
                    break
            self.save(w_tape)
            self.page_generators[r2_tape]=None
            open(r2_tape,'w').close()
            self.merge(t1,w1,record1,None)
        else:
            while True:
                if record2:
                    if self.cmp_values(v2,pv2):
                        pv2=v2
                        break
                    self.save_record(w_tape,record2)
                    pv2=v2
                    record2=self.get_record(r2_tape)
                    if not record2:
                        break
                    v2=self.get_value(record2)
                else:
                    break
            self.save(w_tape)
            self.page_generators[r1_tape]=None
            open(r1_tape,'w').close()
            self.merge(w1,t2,None,record2)

    def sort(self):

        open('tapes/tape1.dat','w').close()
        open('tapes/tape2.dat','w').close()
        open('tapes/tape3.dat','w').close()

        self.number_of_reads=0
        self.number_of_writes=0
        self.number_of_phases=0

        l1,l2,index=self.distribution()
        self.end=index

        print(l1,l2,self.fib_list[index])

        #record=self.first_merge('tapes/tape1.dat',self.fib_list[index]-l1)

        if l1 in self.fib_list and l2 in self.fib_list:
            print('xx')
            self.merge(1,2,None,None,True)
        elif l1 in self.fib_list:
            record=self.first_merge('tapes/tape1.dat',self.fib_list[index]-l2)
            self.merge(1,2,record,None)
            pass
        elif l2 in self.fib_list:
            record=self.first_merge('tapes/tape2.dat',self.fib_list[index]-l1)
            self.merge(1,2,None,record)
        
        else:
            print('-----------------------------')
            if l1>l2:
                print('l1>l2')
                record=self.first_merge('tapes/tape2.dat',self.fib_list[index]-l1)
                if not record:
                    record=self.get_record('tapes/tape1.dat')
                if not record:
                    self.merge(1,2,None,None,True)
                else:
                    self.merge(1,2,None,record)

            else:
                print('l1<l2')
                record=self.first_merge('tapes/tape1.dat',self.fib_list[index]-l2)
                if not record:
                    record=self.get_record('tapes/tape2.dat')
                if not record:
                    self.merge(1,2,None,None,True)
                else:
                    self.merge(1,2,record,None)
        



if __name__=='__main__':
    
    p=PolyphaseSort(1024,'data/source.dat')
    p.sort()
    print(p.number_of_phases)
    print(p.number_of_reads)
    print(p.number_of_writes)