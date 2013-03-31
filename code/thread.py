import threading
import random
import time

def fn1(x,v):
    v.append(x*x)
    print x

def fn(x,v):
    if random.random() > 0.5:
        time.sleep(1)

    '''
    if x == 2:
        v1 = []
        threads1 = []
        for j in range(10):
            threads1.append(threading.Thread(target=fn1, args=(j,v1)))
        for thread in threads1:
            thread.start()

        for thread in threads1:
            #thread.join()
            pass
    '''

    v.append(x)

v = []
threads = []
for i in range(10):
    threads.append(threading.Thread(target=fn, args=(i,v)))

for thread in threads:
    thread.start()

count = 0
for thread in threads:
    thread.join()
    print float(count) / len(threads)
    count += 1
    
print v
time.sleep(2)
print v