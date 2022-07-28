import os
import concurrent.futures
from collections import deque

threadsNum = 6
sensivity_step = 1

def threadFunc(fileName):
    similarities = deque()
    results = deque()

    fileStream = open(fileName, 'r')
    for line in fileStream:
        if (line.startswith("Error") or line.startswith("Code") or len(line) < 2):
            continue
        similarities.append(float(line))

    for sensivity in range(0, 101, sensivity_step):
        counter = 0
        for s in similarities:
            if (s < (sensivity/100)):
                counter += 1
        results.append(counter)

    return results

with concurrent.futures.ThreadPoolExecutor(max_workers=threadsNum) as executor:
    futures = []
    for root, dirs, files in os.walk('FAR-FRR/frr-results'):
        for name in files:
            futures.append(executor.submit(threadFunc, os.path.join(root, name)))  
    print("Started...")              
    for future in concurrent.futures.as_completed(futures):
        continue

fileStream = open("FAR-FRR/processed-frr.txt", 'w')
for i in range(int(101/sensivity_step)):
    sum = 0
    for deq in futures:
        sum += deq.result()[i]
    fileStream.write(f'{sum/60.5}\n')
