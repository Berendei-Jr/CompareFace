from collections import deque
from matplotlib import pyplot as plt
import numpy as np

farY = deque()
frrY = deque()

farStream = open('FAR-FRR/processed-far.txt', 'r')
frrStream = open('FAR-FRR/processed-frr.txt', 'r')

for line in farStream:
    farY.append(float(line))

for line in frrStream:
    frrY.append(float(line))    

x = range(0, 101, 1)
plt.figure(1)
plt.title("FAR/FRR")
plt.xlabel("Sensivity")
plt.ylabel("Mistake probability (%)")
plt.plot(x, farY, label="FAR")

plt.figure(1)
plt.plot(x, frrY, label="FRR")
plt.legend()
plt.grid()

plt.savefig('far-frr-plot.png', dpi = 1000)

for i in range(50):
    farY.popleft()
    frrY.popleft()
for i in range(10):
    farY.pop()
    frrY.pop()    

x = range(50, 91, 1)
plt.figure(2)
plt.title("FAR/FRR")
plt.xlabel("Sensivity (%)")
plt.ylabel("Mistake probability (%)")
plt.plot(x, farY, label="FAR")

plt.figure(2)
plt.plot(x, frrY, label="FRR")
plt.legend()
plt.grid()

plt.savefig('far-frr-plot-zoomed.png', dpi = 1000)    