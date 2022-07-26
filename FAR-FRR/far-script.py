import subprocess
import os
from threading import Thread
from pathlib import Path
from collections import deque

def objectsInFolder(path):
    return len(list(Path(path).iterdir()))

def isValid(file, validFaces):
    for i in validFaces:
        if (file == i):
            return True
    return False        

facesRoot = "/home/hellcat/workspace/lfw"
validFacesNum = 6
threadsNum = 6
peopleNum = len(list(Path(facesRoot).iterdir()))

#Заполнение массива "валидных" лиц
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

#Потоковая функция. Получает на вход массив "валидных" лиц, которые ей нужно будет обработать и массив всех остальных лиц в базе
def threadFunc(i, validFaces_db, faces_db):
    print("Got faces:", len(validFaces_db))

    counter = 0
    for face in validFaces_db:
        for root, dirs, files in os.walk(faces_db):
            for name in files:
                counter += 1
                if (isValid(os.path.join(root, name), validFaces) == False):
                    result = subprocess.run(['/home/hellcat/CLionProjects/CompareFace/cmake-build-debug/compare_face',
                    face, os.path.join(root, name)],
                    stdout=subprocess.PIPE, encoding='utf-8')
                    if (counter % 10 == 0):
                        print('thread', i, ') ', counter, ' ', counter/(peopleNum*len(validFaces_db)) * 100, '%')
                    
                    
#Подготовка массива лиц для каждого потока и запуск потоков
for i in range (threadsNum):
    threadFacesPool = []
    for it in range(validFacesNum):
        if (it%threadsNum == i):
            threadFacesPool.append(validFaces[it])
    th = Thread(target=threadFunc, args=(i, threadFacesPool, facesRoot))
    th.start()
