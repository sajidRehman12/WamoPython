


#             # concurrancy in python
# threads get their own copy as well
# if we use gloabal we change the global copy as well


# import  threading
# x=10

# def func(n,t):
#     print(t)
#     global x 
#     x=x+2
#     print(n)

# t1=threading.Thread(target=func,args=(x,"thread 1 executing"))
# t2=threading.Thread(target=func,args=(x,"thread 2 executing"))
# t3=threading.Thread(target=func,args=(x,"thread 3 executing"))

# t1.start()
# t2.start()
# t3.start()
# t1.join()
# t2.join()
# t3.join()
# print(x)



# processess get their own copy 
# if we use gloabal we cannot still change the global copy
# import multiprocessing
# x=10

# def func(n,t):
#     print(t)
#     global x 
#     x=x+2
#     print(n)

# t1=multiprocessing.Process(target=func,args=(x,"thread 1 executing"))
# t2=multiprocessing.Process(target=func,args=(x,"thread 2 executing"))
# t3=multiprocessing.Process(target=func,args=(x,"thread 3 executing"))

# t1.start()
# t2.start()
# t3.start()
# t1.join()
# t2.join()
# t3.join()
# print(x)



# coding questions of sets dict tuple list map filter reduce lambda


# s = {[1, 2], [3, 4]}
# print(s) error only immutables for sets

# def f(lst=[]):
#     lst.append(1)
#     return lst

# print(f())
# print(f())
# print(f())

# def f(lst=None):
#     if lst is None:
#         lst = []
#     lst.append(1)
#     return lst


# print(f())
# print(f())
# print(f())



# lst = [1, 2, 3, 4, 5, 6]
# for x in lst:
#     if x % 2 == 0:
#         lst.remove(x)
# print(lst) 
# element 6 survived because 
# elements get back when loop so use filter maps etc


# race condition example and cure with lock

# import threading

# counter =0
# lock=threading.Lock()
# def func():
#     global counter 
#     with lock:
#         counter+=1

# t1=threading.Thread(target=func)
# t2=threading.Thread(target=func)

# t1.start()
# t2.start()
# t1.join()
# t2.join()
# print(counter)

# using signals
# import threading, time

# event = threading.Event()

# def waiter(name):
#     print(f"{name}: waiting for signal...")
#     event.wait()                   
#     print(f"{name}: got the signal!")

# def signaler():
#     time.sleep(2)
#     print("Signaler: sending signal!")
#     event.set()                 

# threads = [threading.Thread(target=waiter, args=(f"T{i}",)) for i in range(3)]
# threads.append(threading.Thread(target=signaler))

# for t in threads: t.start()
# for t in threads: t.join()



# from multiprocessing import Manager 
# from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
# import os,pathlib
# def gen():
#     print("Start")
#     yield 1
#     print("Middle")
#     yield 2
#     print("End")


# def gentoreadfile():
#     with open("myfile.txt","r") as f:
#         for line in f:
#             yield line


# class iterator():
#     myCounter=10
#     curr=0
#     def __iter__(self):
#         return self
#     def __next__(self):
#         if self.curr <self.myCounter:
#             curr=self.curr
#             self.curr+=1
#             return curr
#         raise StopIteration 
        
# iter=iterator()

# print(iter)


# l=list([1,2,3,4,5,6,7,7,8,9,])


# d={"key":"value","pair":"pair"}
# def func(**d):
#     d["key"]="changed"
#     print(d)


   
# manager = Manager()

# counter = manager.Value('i', 0)

# def thread_task(counter):
#     counter += 1
#     print(counter)


# def process_task():
#     global counter
#     counter += 1
#     print(f"[Process] PID={os.getpid()} counter={counter}")
#     return counter


# def thread_task(args):
#     counter, = args
#     counter.value += 1  # This is now process-safe

# with Manager() as manager:
#     counter = manager.Value('i', 0)
#     with ProcessPoolExecutor(max_workers=8) as executor:
#         results = list(executor.map(thread_task, [(counter,)] ))

    
    # print(os.getcwd())
    # print(os.listdir())
    # with open("myfile.txt","a") as f:
    #     f.write("this is data from basics.py\n")
    # g=gentoreadfile()
    # while True:
    #     try:
    #         print(next(g))
    #     except StopIteration:
    #         break


    # print(iter)
    # for i in iter:
    #     print(i)
  
#    func( key="value", pair="pair")
#    print(d)
# #    d={ **d,"key":"value","pair":"pair"}



# d={"a":1,"b":2,"c":3}

# for i in d.items():
#     print(i[1])

# # keys=[i[1] for i in d.items()]
# # values=[i[0] for i in d.items()]

# keys= d.keys()
# values= d.values()

# loft=list(zip(values,keys))
 
# print(dict(loft))

# ls=dict(loft)

# print(list(ls))

# from collections import namedtuple
# Point = namedtuple('pint', ['x', 'y'])
# p = Point(3, 4)
# distance = (p.x**2 + p.y**2) ** 0.5
# print(f"Distance from origin: {distance}")  

# lst = [1, [2, 3], [4, [5, 6]]]


# flatlist=[x for x in lst if isinstance(x, list) for x in x]
# flatlist2=[]

# def flatten(lst):
#     result=[]
#     for x in lst:
#         if isinstance(x , list):
#             result.extend(flatten(x))
#         else:
#             result.append(x)
#     return result
# print(flatten(lst))

# lst = [3, 1, 2, 3, 4, 1, 5]
# result= []
# [result.append(x) for x in lst if x not in result] 
# print(result)

# lst = [1, 2, 3, 4, 5]
# k=2
# newlist=lst[2:]+lst[:2]
# print(newlist)


# lst = [1, 2, 3, 4, 5, 6, 7]
# n = 3

# result=[]

# for x in range(0,len(lst),n):  
#     newlist=lst[x:x+n]
#     result.append(newlist)

# print(result)



# lst = [10, 20, 4, 45, 99, 99]
# # Expected output: 45

# print(sorted(list(set(lst)))[-2])


# lst = [(1, 3), (2, 1), (4, 2)]


# sortedTuples=sorted(lst,key=lambda x:x[1],reverse=False)

# print(sortedTuples)

# lst = [(1,2), (3,4), (5,0), (2,2)]
# # Expected output: (3, 4)


# result=max(lst,key=lambda x:x[0]+x[1])

# print(result)

# a = [1, 3, 4]
# b = [2, 3, 5, 6]
# c = [3, 2, 7, 8]
# # Expected output: {2, 3}

# output=set(a) & set(b) &set(c)

# print(output)


# lst = [3, 1, 2, 3, 4, 1, 5]

# removedDuplicates= dict.fromkeys(lst)

# print(list(removedDuplicates.keys()))

# a = {1, 2, 3, 4, 5}
# b = {3, 4, 5, 6, 7}
# # Expected output: {1, 2}

# print(a-b)

# s = "programming"

# print(''.join(set(s)))

# words = ['hi', 'hello', 'hey', 'world', 'ok']
# groupdict={}

# for word in words:
#     groupdict[len(word)]=groupdict.get(len(word),[])+ [word]
# print(groupdict)


# lst = [1, 2, 3, 2, 1, 2, 3, 1, 1]
# freq={}

# for x in lst:
#     freq[x]=freq.get(x,0)+1
# print(freq)

# result=max(freq.items(),key=lambda x:x[1])
# print(result[0])

# d = {'banana': 3, 'apple': 5, 'cherry': 1}

# print(dict(sorted(d.items(),key=lambda x: x[1],reverse=True)))

# s = "hello world"

# freq={}
# for x in s:
#     freq[x] = freq.get(x,0)+1

# print(freq)


# lst = [1, 2, 3, 4, 5]
# print(list(map(lambda x:x**2,lst)))

# a = [1, 2, 3]
# b = [4, 5, 6]
# c=[5,6,7,8]

# print(list(map(lambda x,y,z:x+y+z,a,b,c)))


# lst = ['hello', 'world', 'python']

# print(list(map(lambda word: word.upper(),lst)))


