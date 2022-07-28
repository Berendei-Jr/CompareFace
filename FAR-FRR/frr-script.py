import subprocess
import os
import concurrent.futures
from pathlib import Path
from collections import deque
from datetime import datetime
import threading

def objectsInFolder(path):
    return len(list(Path(path).iterdir()))

def isValid(file, validFaces):
    for i in validFaces:
        if (file == i):
            return True
    return False        

facesRoot = "/home/hellcat/workspace/lfw"
threadsNum = 6
peopleNum = len(list(Path(facesRoot).iterdir()))

logStream = open('FAR-FRR/logs.txt', 'w')

print(f'Looking for valid faces...')      
# Заполнение массива "валидных" лиц
validFaces = deque()
i = 0
for root, dirs, files in os.walk(facesRoot):
    if (root == '/home/hellcat/workspace/lfw'):
        continue
    if (objectsInFolder(root) > 1):
        result = subprocess.run(['cmake-build-debug/detect_face',
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
   # print("Got faces:", facesNum)

    results = []
    fileStream = open(f'FAR-FRR/frr-results/{threading.current_thread().name}.txt', 'w')

    counter = 0
    for face_root in validFaces_db:
        if (counter%10 == 0):
            print(threading.current_thread().name, ': ', counter)

        for root, dirs, files in os.walk(face_root):
            for name in files:
                if (name == files[0]):
                    continue
                result = subprocess.run(['cmake-build-debug/compare_face',
                os.path.join(root, files[0]), os.path.join(root, name)],
                stdout=subprocess.PIPE, encoding='utf-8')
                logStream.write(f'{os.path.join(root, files[0])} + {os.path.join(root, name)}\n')
                results.append(result.stdout)
   #                 print(threading.current_thread().name, ': ', counter)
        counter += 1

    for i in results:
        fileStream.write(i + '\n')
    fileStream.close()     

start_time = datetime.now()
# Подготовка массива лиц для каждого потока и запуск потоков
with concurrent.futures.ThreadPoolExecutor(max_workers=threadsNum) as executor:
    futures = []
    for i in range (threadsNum):
        threadFacesPool = []
        for it in range(len(validFaces)):
            if (it % threadsNum == i):
                threadFacesPool.append(validFaces[it])
        futures.append(executor.submit(threadFunc, threadFacesPool))  
    print("Started...")              
    for future in concurrent.futures.as_completed(futures):
        continue

print(datetime.now() - start_time)
