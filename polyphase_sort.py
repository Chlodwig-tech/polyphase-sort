import sys
import os
import print_file

class PolyphaseSort:

    def __init__(self,page_size,source,destination,debug=False,sort_ascending=True):
        self.number_of_reads=0
        self.number_of_writes=0
        self.number_of_phases=0
        self.number_of_runs=0
        self.fib_list=[1,1]

        self.page_generators={}
        self.records_generators={}
        self.tapes={}
        
        self.page_size=page_size
        self.source=source
        self.destination=destination
        self.stop=False
        self.debug=debug
        self.sort_ascending=sort_ascending

        self.page_generators[source]=None

        self.sorted=False

        for i in range(3):
            self.tapes[f'tapes/tape{i+1}.dat']=''
            self.page_generators[f'tapes/tape{i+1}.dat']=None
            self.records_generators[f'tapes/tape{i+1}.dat']=None

        self.t1,self.t2,self.r1,self.r2=None,None,None,None

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
            return next(self.records_generators[path])
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

        if self.debug:
            print('After distribution:')
            print_file.print_file('tapes/tape1.dat',self.page_size)
            for value,elem in zip(print_file.l,print_file.l3):
                print(elem,value)
            print_file.l,print_file.l3=[],[]
            print('---------')
            print_file.print_file('tapes/tape2.dat',self.page_size)
            for value,elem in zip(print_file.l,print_file.l3):
                print(elem,value)
            print_file.l,print_file.l3=[],[]
            print('-------------------------')

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

    def merge(self):
        self.number_of_phases+=1
        
        r1_tape,r2_tape=f'tapes/tape{self.t1}.dat',f'tapes/tape{self.t2}.dat'
        w1=1 if (self.t1==2 and self.t2==3) or (self.t1==3 and self.t2==2) else 2 if (self.t1==1 and self.t2==3) or (self.t1==3 and self.t2==1) else 3
        w_tape=f'tapes/tape{w1}.dat'

        record1,record2=self.r1,self.r2

        if not record1 and not record2 and self.dummy_series:
            self.sorted=True
            self.number_of_phases-=1
            if os.stat(r1_tape).st_size==os.stat(self.source).st_size:
                if os.name=='nt':
                    os.system(f'copy {r1_tape} {self.destination}')
                else:
                    os.system(f'cp {r1_tape} {self.destination}')
            else:
                if os.name=='nt':
                    os.system(f'copy {r2_tape} {self.destination}')
                else:
                    os.system(f'cp {r2_tape} {self.destination}')
            return
        
        if not self.dummy_series:
            self.dummy_series=True

        self.init_generator(r1_tape)
        self.init_generator(r2_tape)

        pv1,pv2=None,None
        r1,r2=True,True
        x1,x2=False,False

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

            if self.debug:
                print(f'After {self.number_of_phases} merge:')
                print_file.print_file(r1_tape,self.page_size)
                for value,elem in zip(print_file.l,print_file.l3):
                    print(elem,value)
                print_file.l,print_file.l3=[],[]
                print('---------')
                print_file.print_file(w_tape,self.page_size)
                for value,elem in zip(print_file.l,print_file.l3):
                    print(elem,value)
                print_file.l,print_file.l3=[],[]
                print('-------------------------')

            self.page_generators[r2_tape]=None
            open(r2_tape,'w').close()
            self.t1,self.t2,self.r1,self.r2=self.t1,w1,record1,None
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
            if self.debug:
                print(f'After {self.number_of_phases} merge:')
                print_file.print_file(r2_tape,self.page_size)
                for value,elem in zip(print_file.l,print_file.l3):
                    print(elem,value)
                print_file.l,print_file.l3=[],[]
                print('---------')
                print_file.print_file(w_tape,self.page_size)
                for value,elem in zip(print_file.l,print_file.l3):
                    print(elem,value)
                print_file.l,print_file.l3=[],[]
                print('-------------------------')
            self.page_generators[r1_tape]=None
            open(r1_tape,'w').close()
            self.t1,self.t2,self.r1,self.r2=w1,self.t2,None,record2

    def sort(self):

        for key in self.page_generators:
            self.page_generators[key]=None
        for key in self.records_generators:
            self.records_generators[key]=None
        for key in self.tapes:
            self.tapes[key]=''

        open('tapes/tape1.dat','w').close()
        open('tapes/tape2.dat','w').close()
        open('tapes/tape3.dat','w').close()

        self.number_of_reads=0
        self.number_of_writes=0
        self.number_of_phases=0
        self.sorted=False

        l1,l2,index=self.distribution()

        self.number_of_runs=l1+l2
        x=0
        record1,record2=None,None
        self.dummy_series=True

        if l1 in self.fib_list and l2 in self.fib_list:
            self. dummy_series=False
        elif l1 in self.fib_list:
            self.r1=self.first_merge('tapes/tape1.dat',self.fib_list[index]-l2)
            x=self.fib_list[index]-l2
        elif l2 in self.fib_list:
            self.r2=self.first_merge('tapes/tape2.dat',self.fib_list[index]-l1)
            x=self.fib_list[index]-l1

        self.t1,self.t2=1,2
        
        while not self.sorted:
            self.merge()

        print(f'Number of runs: {self.number_of_runs}({x}) | {l1}-{l2}')
        print(f'Number of reads: {self.number_of_reads}')
        print(f'Number of writes: {self.number_of_writes}')
        print(f'Number of phases: {self.number_of_phases}')

if __name__=='__main__':
    
    p=PolyphaseSort(1024,'data/source.dat','data/destination.dat')
    p.sort()