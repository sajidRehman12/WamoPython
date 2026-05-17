


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

import threading

counter =0
lock=threading.Lock()
def func():
    global counter 
    with lock:
        counter+=1

t1=threading.Thread(target=func)
t2=threading.Thread(target=func)

t1.start()
t2.start()
t1.join()
t2.join()
print(counter)