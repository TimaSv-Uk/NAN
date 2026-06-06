simmilar to RCA algorithm for shift
ring z512

multiplicative group 
1,3,5,7 ...


x mod128 переходить 2x-1 mod512

512 half element with no pair

z256 
0, 1 ,2 ,... 255

F =  x mod256 > 2x-1 mod 512
1 > 2*1-1 



when number more then 512 we use mod 512

512 half element with no pair we get only not 256 and compere them with assci

F - 1 
s512 > x 256

7 = (7-1)/2 and so on


## Encoding algo

whe take graph

z512*(and not paired) ^ n


points() and lines[]
where was  - we use *

x2*y2 = y1*x1
x3*y3 = x1*y2
x4*y4 = x1*y3
...
x5*y5 = x1*y4


x1 ^ a1(alpha) where a1 mod 256
[y1,y2,yn]

Take paired length vencor a1...ak

x1,x2,xn
neigbors with color x1^a1


a1 diffirent from a3, a5 diff from a7

old
x1+x2+...xn

new 
x1*x2*...xn

NOTE:
Last element ak must be no paired so we can decode
a[] we get from elemnts of molulo 256


MAYBE LATER:
filed 256 and change - to +, or - to *, group of 255 with no 0
advantege of this files will be with ^n,attacker will have tougher time aproximationg algorithm



