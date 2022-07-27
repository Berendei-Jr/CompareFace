import subprocess
import os
import concurrent.futures
from pathlib import Path
from collections import deque
#from datetime import datetime
import threading

def objectsInFolder(path):
    return len(list(Path(path).iterdir()))

def isValid(file, validFaces):
    for i in validFaces:
        if (file == i):
            return True
    return False        

facesRoot = "/home/hellcat/workspace/lfw"
validFacesNum = 200
candidatesNum = 1000
threadsNum = 6
peopleNum = len(list(Path(facesRoot).iterdir()))

print(f'Looking for {validFacesNum} valid faces...')      
# Заполнение массива "валидных" лиц
validFaces = deque()
i = 0
for root, dirs, files in os.walk(facesRoot):
    if (objectsInFolder(root) == 1):
        result = subprocess.run(['/home/hellcat/CLionProjects/CompareFace/cmake-build-debug/detect_face',
            os.path.join(root, files[0])], stdout=subprocess.PIPE, encoding='utf-8')
        if (int(result.stdout) == 1):    
            i+=1
            validFaces.append(os.path.join(root, files[0]))
            if (i == validFacesNum):
                break

# Потоковая функция. Получает на вход массив "валидных" лиц, которые ей нужно будет обработать и массив всех остальных лиц в базе
def threadFunc(validFaces_db, faces_db):
    facesNum = len(validFaces_db)
    #print("Got faces:", facesNum)

    results = []
    fileStream = open(f'{threading.current_thread().name}.txt', 'w')

    counter = 0
    for face in validFaces_db:
        if (counter%3):
            if (threading.current_thread().name == "ThreadPoolExecutor-0_1"):
                print(f'{counter/facesNum * 100}%')

        candidatesCounter = 0
        for root, dirs, files in os.walk(faces_db):
            for name in files:
                if (candidatesCounter >= candidatesNum):
                    break
                if (isValid(os.path.join(root, name), validFaces) == False):
                    result = subprocess.run(['/home/hellcat/CLionProjects/CompareFace/cmake-build-debug/compare_face',
                    face, os.path.join(root, name)],
                    stdout=subprocess.PIPE, encoding='utf-8')
                    results.append(result.stdout)
                    candidatesCounter += 1
                    #print(threading.current_thread().name, ': ', counter)
        counter += 1

    for i in results:
        fileStream.write(i + '\n')
    fileStream.close()     

#start_time = datetime.now()
# Подготовка массива лиц для каждого потока и запуск потоков
with concurrent.futures.ThreadPoolExecutor(max_workers=threadsNum) as executor:
    futures = []
    for i in range (threadsNum):
        threadFacesPool = []
        for it in range(validFacesNum):
            if (it % threadsNum == i):
                threadFacesPool.append(validFaces[it])
        futures.append(executor.submit(threadFunc, threadFacesPool, facesRoot))  
    print("Started...")              
    for future in concurrent.futures.as_completed(futures):
        continue

#print(datetime.now() - start_time)
