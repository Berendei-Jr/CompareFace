import subprocess
import os
import concurrent.futures
from pathlib import Path
from collections import deque
import threading

def objectsInFolder(path):
    return len(list(Path(path).iterdir()))

def isValid(file, validFaces):
    for i in validFaces:
        if (file == i):
            return True
    return False        

facesRoot = "faces_db/lfw"
threadsNum = 6
peopleNum = len(list(Path(facesRoot).iterdir()))

print(f'Looking for valid faces...')      
# Заполнение массива "валидных" лиц
validFaces = deque()
i = 0
for root, dirs, files in os.walk(facesRoot):
    if (root == 'faces_db/lfw'):
        continue
    if (objectsInFolder(root) > 1):
        result = subprocess.run(['_build/detect_face',
            os.path.join(root, files[0])], stdout=subprocess.PIPE, encoding='utf-8')
        if (result.stdout == "1"):    
            i+=1
            validFaces.append(root)
            if (i % 10 == 0):
                print(f'Found {i} faces...')      

print(f'TOTAL FACES: {i}')                

# Потоковая функция. Получает на вход массив "валидных" лиц, которые ей нужно будет обработать и массив всех остальных лиц в базе
def threadFunc(validFaces_db):
    facesNum = len(validFaces_db)
   
    results = []
    fileStream = open(f'FAR-FRR/frr-raw-results/{threading.current_thread().name}.txt', 'w')

    counter = 0
    for face_root in validFaces_db:
        if (counter%10 == 0):
            if (threading.current_thread().name == "ThreadPoolExecutor-0_0"):
                print(f'{counter/facesNum * 100}%')

        for root, dirs, files in os.walk(face_root):
            for name in files:
                if (name == files[0]):
                    continue
                result = subprocess.run(['_build/compare_face',
                os.path.join(root, files[0]), os.path.join(root, name)],
                stdout=subprocess.PIPE, encoding='utf-8')
                results.append(result.stdout)
        counter += 1

    for i in results:
        fileStream.write(i + '\n')
    fileStream.close()     

# Подготовка массива лиц для каждого потока и запуск потоков
with concurrent.futures.ThreadPoolExecutor(max_workers=threadsNum) as executor:
    futures = []
    print("Step 1: Started...")  
    for i in range (threadsNum):
        threadFacesPool = []
        for it in range(len(validFaces)):
            if (it % threadsNum == i):
                threadFacesPool.append(validFaces[it])
        futures.append(executor.submit(threadFunc, threadFacesPool))              
    for future in concurrent.futures.as_completed(futures):
        continue

print("Step 1: Finished!\nStep 2: Started...")
sensivity_step = 1

def threadFunc1(fileName):
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
    for root, dirs, files in os.walk('FAR-FRR/frr-raw-results'):
        for name in files:
            futures.append(executor.submit(threadFunc1, os.path.join(root, name)))  
    for future in concurrent.futures.as_completed(futures):
        continue

fileStream = open("FAR-FRR/frr_processed_results/processed-frr.txt", 'w')
for i in range(int(100/sensivity_step)):
    sum = 0
    for deq in futures:
        sum += deq.result()[i]
    fileStream.write(f'{sum/60.5}\n')
  
print("Step 2: Finished!") 
