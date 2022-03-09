

t = {(1,1): 0}
b = [1,1]
print(t[tuple(b)])



"""
import numpy as np


arr1 = np.array([[j*10+i for i in range(10)] for j in range(5)])
arr2 = np.array([[i*10+j for i in range(10)] for j in range(5)])

cycled = np.zeros(arr1.shape[0], dtype = int)

step = 1


print(f'---------------------- {step = } ---------------------------')
print(arr1)
print()
print(arr2)
print()
s = np.sum((arr1 - arr2 != 0),axis = 1 ) == 0; step += 1
print(s)
print()
cycled[cycled==0] = s[cycled==0] * step
print(cycled)


arr2[0,:] = np.array([i for i in range(10)])
s = np.sum((arr1 - arr2 != 0),axis = 1 ) == 0; step += 1
print(f'---------------------- {step = } ---------------------------')
print(arr1)
print()
print(arr2)
print()
print(s)
cycled[cycled==0] = s[cycled==0] * step
print(cycled)


arr2[0,:] = np.array([i for i in range(10)])
s = np.sum((arr1 - arr2 != 0),axis = 1 ) == 0; step += 1
print(f'---------------------- {step = } ---------------------------')
print(arr1)
print()
print(arr2)
print()
print(s)
cycled[cycled==0] = s[cycled==0] * step
print(cycled)

arr2[1,:] = np.array([10+i for i in range(10)])
arr2[2,:] = np.array([20+i for i in range(10)])


s = np.sum((arr1 - arr2 != 0),axis = 1 ) == 0; step += 1
print(f'---------------------- {step = } ---------------------------')
print(arr1)
print()
print(arr2)
print()
print(s)
cycled[cycled==0] = s[cycled==0] * step
print(cycled)

s = np.sum((arr1 - arr2 != 0),axis = 1 ) == 0; step += 1
print(f'---------------------- {step = } ---------------------------')
print(arr1)
print()
print(arr2)
print()
print(s)
cycled[cycled==0] = s[cycled==0] * step
print(cycled)

arr2[3,:] = np.array([30+i for i in range(10)])

s = np.sum((arr1 - arr2 != 0),axis = 1 ) == 0; step += 1
print(f'---------------------- {step = } ---------------------------')
print(arr1)
print()
print(arr2)
print()
print(s)
cycled[cycled==0] = s[cycled==0] * step
print(cycled)

arr2[4,:] = np.array([40+i for i in range(10)])

s = np.sum((arr1 - arr2 != 0),axis = 1 ) == 0; step += 1
print(f'---------------------- {step = } ---------------------------')
print(arr1)
print()
print(arr2)
print()
print(s)
cycled[cycled==0] = s[cycled==0] * step
print(cycled)

print( arr1[:,5:] )
print()
print( arr1[:,:5] )
print()
print(arr1[:,5:] + arr1[:,:5])

w,h = 6,4
arr3 = np.array([[ 13, -13,  -2,   0,   0,   0],
                 [ 16,   2, -15,   0,   0,   0],
                 [  7, -18, -12,   0,   0,   0],
                 [ -3,  -8,  -8,   0,   0,   0]])
arr3[:,2] = 0
for i in range(h):
    r = np.r_[0:i, i+1:arr3.shape[0]]
    # print(arr3)
    # print('-', arr3[i,:3] > arr3[r,:3])
    # print()
    # print('-', arr3[i,:3] < arr3[r,:3])
    print()
    print(arr3)
    print()

    print(arr3[i])
    print(np.sum(arr3[i,:3] < arr3[r,:3], axis=0))
    print(np.sum(arr3[i,:3] > arr3[r,:3], axis=0)*-1)
    arr3[i,3:] += np.sum(arr3[i,3:] < arr3[r,:3], axis=0) - np.sum(arr3[i,:3] > arr3[r,:3], axis=0)
    print(arr3[i])

    # print( arr3 )






"""


#