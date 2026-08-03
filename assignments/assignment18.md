





# TODO:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::TODAY



## in addintion to new algorithsms and tests
**DONE**
- refactor encode,decode algorithsms **to class based** approach 
- refactor **encode_decode.py** so it fits class based algorithsms
- refactor **tests** so it fits class based algorithsms

**TODO**
- redo **finite_field precalc** Fn with no 0, exclude 0
    - HINT: fiead of 255 only odd numbers,z2^6 -> z2^7

    - PROBLEM: I can not map 254 numbers to 255, if i remove zero from the table and then try to encode and decode without zero condition, i figure i wont be able to decode enything 
    (Table would only have indices from 0 to 254. If  data contains the byte 255, the code will try to look up row or column 255, crash, and throw an "index out of bounds" error.)
- make encoding classes : - to +, or - to *, group of 255 with no 0
    - encode_decode.py modification
    - test them

## new algorithsms and tests

- to +, or - to *, group of 255 with no 0

new algo based on finite_field version

Fn with no 0, exclude 0
Result shoud contain 2 version of algorithm with:
    - to *
    - to +

fiead of 255 only odd numbers
z2^6 -> z2^7

later:
x and y in some^ 

Idea for later:
ring Fq - enlage finite field by adding многочлени
кільце многоленів з багатьох змінних

take our graph
first step
1. make a new Ring  Fq  = [x1, x2, xn]

Graph an k
2. replace original ring k with Fq

polinomial [x1, x2, xn]
vector (x1, x2, xn) straigt
x1 + a1,x2 + a2, x3 + a3


Example of graphs path 
F1 [x1]
F2 [x1, x2]
Fm [x1, x2,... xm]

------
Rules of tranformation of field Fq

x1 -> F1 [x1]
x2 -> F2 [x1, x2]
xm -> Fm [x1, x2,... xm]

------
after we multiply by our matrix form left and right side
x1 -> G1 (x1 x2 xm)

transormation ^3, cubical
G will serve as a public key
