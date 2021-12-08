def first_merge(self,path,n):
    open('tapes/tape3.dat','w').close()
    self.init_generator(path)
    record=self.get_record(path)
    v=self.get_value(record)
    for i in range(n):
        pv=None
        while True:
            if record:
                if self.cmp_values(v,pv):
                    break
                self.save_record('tapes/tape3.dat',record)
                pv=v
                record=self.get_record(path)
                v=self.get_value(record)
            else:
                return None
    return record

def first_merge(self,path,n):
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

def merge(self,t1,t2,record1,record2):
    print('n: ',self.number_of_phases)
    self.number_of_phases+=1
    
    r1_tape,r2_tape=f'tapes/tape{t1}.dat',f'tapes/tape{t2}.dat'
    w1=1 if (t1==2 and t2==3) or (t1==3 and t2==2) else 2 if (t1==1 and t2==3) or (t1==3 and t2==1) else 3
    w_tape=f'tapes/tape{w1}.dat'

    if not record1 and not record2:
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










def distribution(self):
    open('tapes/tape1.dat','w').close()
    open('tapes/tape2.dat','w').close()

    self.init_generator(self.source)

    index,counter=0,1
    t=True
    p_v=None
    len1,len2=0,0

    while True:
        record=self.get_record(self.source)
        if not record:
            if t:
                len1+=1
            else:
                len2+=1
            break
        value=self.get_value(record)
        if self.cmp_values(value,p_v):
            if t:
                len1+=1
            else:
                len2+=1
            counter-=1
            if counter<=0:
                if index>=len(self.fib_list):
                    self.get_10_more_fib_numbers()
                counter=self.fib_list[index]
                index+=1
                t=not t
        p_v=value
        self.save_record(f'tapes/tape{1 if t else 2}.dat',record)

    self.save('tapes/tape1.dat')
    self.save('tapes/tape2.dat')

    return len1,len2,index