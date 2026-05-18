


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



 
import os,pathlib
def gen():
    print("Start")
    yield 1
    print("Middle")
    yield 2
    print("End")


def gentoreadfile():
    with open("myfile.txt","r") as f:
        for line in f:
            yield line
class iterator():
    myCounter=10
    curr=0
    def __iter__(self):
        return self
    def __next__(self):
        if self.curr <self.myCounter:
            curr=self.curr
            self.curr+=1
            return curr
        raise StopIteration 
        
iter=iterator()

print(iter)


l=list([1,2,3,4,5,6,7,7,8,9,])


d={"key":"value","pair":"pair"}
def func(**d):
    d["key"]="changed"
    print(d)

if __name__ == "__main__":
  
    print(os.getcwd())
    print(os.listdir())
    with open("myfile.txt","a") as f:
        f.write("this is data from basics.py\n")
    g=gentoreadfile()
    while True:
        try:
            print(next(g))
        except StopIteration:
            break


    # print(iter)
    # for i in iter:
    #     print(i)
  
#    func( key="value", pair="pair")
#    print(d)
# #    d={ **d,"key":"value","pair":"pair"}



