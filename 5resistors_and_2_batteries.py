import numpy as np
from scipy.optimize import fsolve
#values could be changed giving other results, these are the random values I assigned.
#usually resistance of the battery is smaller than of the resistor
#c in r1c, and so on means constant (r used in first part of the exercise)
r1c = 11 #ohms
R2c = 12 #ohms
R3c = 13 #ohms
r4c = 14 #ohms
R5c = 15 #ohms
R6c = 16 #ohms
R7c = 17 #ohms
E1 = 5 #V
E4 = 40 #V
k = 0.1 #ohms/A #instead of these kp 0.1 and kn -0.1 coefficients i have one k coefficient with minus or plus sign
#part a) of the exercise
def linear(r1c,R2c,R3c,r4c,R5c,R6c,R7c,E1,E4):
    A = np.array([[r1c+R2c+R3c,r4c,r1c],[-r1c-R6c,R6c,-r1c-R6c-R7c],[-R6c-R5c,r4c+R5c+R6c,-R6c]]) 
    B = np.array([[E4-E1],[E1],[E4]])
    #it should be written in report why such values of A and B were accepted 
    results = np.linalg.solve(A,B) #popular method of solving linear equations
    I3 = results[0] #these three values will be needed later
    I4 = results[1]
    I7 = results[2]
    print("LINEAR VALUES") 
    #why these values are equal to those values is because of mathematics and physics, not programming
    print(f'I1={round(float(results[0]+results[2]),2)} I2={round(float(results[0]),2)}\
    I3={round(float(results[0]),2)}\
    I4={round(float(results[1]),2)} I5={round(float(results[1]-results[0]),2)}\
    I6={round(float(-results[0]-results[2]+results[1]),2)} I7={round(float(results[2]),2)} [Amperes]')
    return((I3),(I4),(I7))
#I decided to use the values of I3, I4, and I7 from previous part, as this first guess that should be given in fsolve    
xyz0 = linear(r1c,R2c,R3c,r4c,R5c,R6c,R7c,E1,E4) 
print(f'reasonable guesses: I3={xyz0[0]} I4={xyz0[1]} I7={xyz0[2]}')
#Nonlinear part of the exercise 
#now values of all resistances depend on the current, so using np.linalg.solve would not be possible (it's no longer linalg, but nonlinalg)
#fsolve is a good way of solving nonlinear equations, especially if you can guess the approximation of the result
def nonlinear(xyz): #function used in fsolve, it will search for values of I3, I4, and I7 until f0, f1, and f2 are almost equal 0
    I3 = xyz[0]
    I4 = xyz[1]
    I7 = xyz[2]
    #mathematics
    f0 = I3*(r1c+R2c+R3c+k*(-I3-I7))+I4*(-k*I4+r4c)+I7*(r1c+k*(-I3-I7))+E1-E4
    f1 = I3*(-r1c-R6c+k*(2*I7+2*I3-I4)+I4*(+R6c+k*(-I3-I7+I4))+I7*(-r1c-R6c-R7c+k*(2*I3-I4+I7)))-E1
    f2 = I3*(-R6c-R5c+k*I7)+I4*(r4c+R5c+R6c+k*(-I4-I7))+I7*(-R6c+k*(I3+I7-I4))-E4
    #to check the value of error of fsolve. the last row should give really small values such as sth * 10^-12 or smaller
    #print(f0,f1,f2) 
    return np.array([f0,f1,f2])
fsolver = fsolve(nonlinear,np.array([xyz0])) #fsolve function finds numerically roots of equation/system of equations with some starting estimate np.array([xyz0]) 
#in this case it is also needed to provide a function (called nonlinear in this program)
I1 = fsolver[0]+fsolver[2]
I2 = fsolver[0]
I3 = fsolver[0]
I4 = fsolver[1]
I5 = fsolver[1]-fsolver[0]
I6 = fsolver[0]+fsolver[2]-fsolver[1]
I7 = fsolver[2]
print("NONLINEAR VALUES")
print(f'I1={round(float(fsolver[0]+fsolver[2]),2)} I2={round(float(fsolver[0]),2)}\
    I3={round(float(fsolver[0]),2)}\
    I4={round(float(fsolver[1]),2)} I5={round(float(fsolver[1]-fsolver[0]),2)}\
    I6={round(float(-fsolver[0]-fsolver[2]+fsolver[1]),2)} I7={round(float(fsolver[2]),2)} [Amperes]')