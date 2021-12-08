def merge2(self,t1,t2):
    r1_tape,r2_tape=f'tapes/tape{t1}.dat',f'tapes/tape{t2}.dat'
    w1=1 if t1==2 and t2==3 else 2 if t1==1 and t2==3 else 3
    w_tape=f'tapes/tape{w1}.dat'

    open(w_tape,'w').close()

    self.init_generator(r1_tape)
    self.init_generator(r2_tape)

    p_v1,p_v2=None,None
    r1,r2=True,True
    record1,record2=None,None


    while True:
        if r1:
            record1=self.get_record(r1_tape)
            if record1:
                v1=self.get_value(record1)
                r1=False
                if self.cmp_values(v1,p_v1):
                    record2=self.complete_run(w_tape,r2_tape,p_v2)
                    if not record2:
                        r2=True
                    else:
                        v2=self.get_value(record2)
                        p_v2=v2
                p_v1=v1
            else:
                break

        if r2:
            record2=self.get_record(r2_tape)
            if record2:
                v2=self.get_value(record2)
                r2=False
                if self.cmp_values(v2,p_v2):
                    self.save_record(w_tape,record1)
                    record1=self.complete_run(w_tape,r1_tape,p_v1)
                    if not record1:
                        r1=True
                    else:
                        v1=self.get_value(record1)
                        p_v1=v1
                p_v2=v2
            else:
                break

        if self.cmp_values(v1,v2):
            self.save_record(w_tape,record1)
            r1=True
        else:
            self.save_record(w_tape,record2)
            r2=True

    self.save(w_tape)

    if record1:
        open(r2_tape,'w').close()
        while record1:
            self.save_record(r2_tape,record1)
            record1=self.get_record(r1_tape)
        self.save(r2_tape)

        self.page_generators[r1_tape]=None
        self.page_generators[r2_tape]=None

        self.merge(t2,w1)
    elif record2:
        open(r1_tape,'w').close()
        while record2:
            self.save_record(r1_tape,record2)
            record2=self.get_record(r2_tape)
        self.save(r1_tape)

        self.page_generators[r1_tape]=None
        self.page_generators[r2_tape]=None

        self.merge(t1,w1)

def dummy_merge(self,path,n):
    self.init_generator(path)
    pv=None
    record=None
    for i in range(n):
        if record:
            self.save_record('tapes/tape3.dat',record)
        record=self.complete_run('tapes/tape3.dat',path,pv)
        if not record:
            return None
        pv=self.get_value(record)

    return record

def merge(self,t1,t2,record1=None,record2=None):
    r1_tape,r2_tape=f'tapes/tape{t1}.dat',f'tapes/tape{t2}.dat'
    w1=1 if t1==2 and t2==3 else 2 if t1==1 and t2==3 else 3
    w_tape=f'tapes/tape{w1}.dat'

    open(w_tape,'w').close()

    self.init_generator(r1_tape)
    self.init_generator(r2_tape)

    p_v1,p_v2=None,None
    r1,r2=True,True
    if record1:
        r1=False
        v1=self.get_value(record1)
        p_v1=v1
    if record2:
        r2=False
        v2=self.get_value(record2)

    while True:
        if r1:
            record1=self.get_record(r1_tape)
            if record1:
                v1=self.get_value(record1)
                r1=False
                if self.cmp_values(v1,p_v1):
                    record2=self.complete_run(w_tape,r2_tape,p_v2)
                    if not record2:
                        r2=True
                    else:
                        v2=self.get_value(record2)
                        p_v2=v2
                p_v1=v1
            else:
                if record2:
                    self.save_record(w_tape,record2)
                record2=self.complete_run(w_tape,r2_tape,p_v2)
                break

        if r2:
            record2=self.get_record(r2_tape)
            if record2:
                v2=self.get_value(record2)
                r2=False
                if self.cmp_values(v2,p_v2):
                    self.save_record(w_tape,record1)
                    record1=self.complete_run(w_tape,r1_tape,p_v1)
                    if not record1:
                        r1=True
                    else:
                        v1=self.get_value(record1)
                        p_v1=v1
                p_v2=v2
            else:
                if record1:
                    self.save_record(w_tape,record1)
                record1=self.complete_run(w_tape,r1_tape,p_v1)
                break

        if self.cmp_values(v1,v2):
            self.save_record(w_tape,record1)
            r1=True
        else:
            self.save_record(w_tape,record2)
            r2=True

    self.save(w_tape)

    if record1:
        open(r2_tape,'w').close()
        while record1:
            self.save_record(r2_tape,record1)
            record1=self.get_record(r1_tape)
        self.save(r2_tape)

        self.page_generators[r1_tape]=None
        self.page_generators[r2_tape]=None

        self.merge(t2,w1)
    elif record2:
        open(r1_tape,'w').close()
        while record2:
            self.save_record(r1_tape,record2)
            record2=self.get_record(r2_tape)
        self.save(r1_tape)

        self.page_generators[r1_tape]=None
        self.page_generators[r2_tape]=None

        self.merge(t1,w1)

def complete_run(self,destination,source,pv):
    while True:
        record=self.get_record(source)
        if record:
            v=self.get_value(record)
            if self.cmp_values(v,pv):
                return record
            else:
                self.save_record(destination,record)
            pv=v
        else:
            return None
    return None

def sort(self):
    self.number_of_reads=0
    self.number_of_writes=0
    l1,l2=self.distribution()
    i=0
    v=0
    if l1>=l2:
        for i in range(len(self.fib_list)):
            if l1<self.fib_list[i]:
                v=i
                break
        record=self.dummy_merge('tapes/tape1.dat',self.fib_list[v]-l1)
        self.merge(1,2,record,None)

    elif l1<l2:
        for i in range(len(self.fib_list)):
            if l2<self.fib_list[i]:
                v=i
                break
        self.dummy_merge('tapes/tape2.dat',self.fib_list[v]-l2)
        self.merge(1,2,None,record)