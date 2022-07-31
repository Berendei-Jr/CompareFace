![](https://github.com/Berendei-Jr/CompareFace/actions/workflows/test_build.yaml/badge.svg)
# FAR/FRR для биометрической системы распознования лиц [CompreFace](https://github.com/exadel-inc/CompreFace)

Для получения результата необходимо, чтобы docker-контейнер фреймворка [CompreFace](https://github.com/exadel-inc/CompreFace#getting-started-with-compreface) был запущен (приложение должно быть доступно по адресу http://localhost:8000)  
Также, в системе должны присутствовать утилиты ```cmake, make, gcc, pip```  
## Инструкция по получению FAR/FRR:
1. Запустите скрипт ```./setup``` (он загрузит тестовую базу данных лиц и правильно скомпилирует 2 утилиты из исходного кода):
    
        > compare_face (принимает 2 фото и возвращает значение similarity)
        > detect_face (принимает 1 фото и возвращает количество обнаруженных на фото лиц)
2. Перейдите в папку FAR-FRR
3. Запустите скрипт ```far-script.py``` (он производит попарные сравнения лиц по следующему правилу:  
  а) Отбирается ```validFacesNum``` фотографий людей, у которых НЕТ других фото и на фото которых присутствует РОВНО 1 лицо)  
  б) Для каждого из этих людей производятся ```candidatesNum``` сравнений с другими людьми  
  > Скрипт записывает значения similarity в папку far-raw-results и обработанные результаты для построения графика в папку far_processed_results (количество сравнений с показателем similarity ВЫШЕ уровня чувствительности)  
4. Запустите скрипт ```frr-script.py``` (он отбирает всех людей из базы данных, у кого более 1 фото и сравнивает фотографии этого человека между собой)
  > Скрипт записывает значения similarity в папку frr-raw-results и обработанные результаты для построения графика в папку frr_processed_results (количество сравнений с показателем similarity НИЖЕ уровня чувствительности)

5. Запустите скрипт ```plot.py``` (он сгенерирует график far-frr в полном масштабе и приближенный в точке пересечения):  
![Full size](https://github.com/Berendei-Jr/CompareFace/blob/master/FAR-FRR/far-frr-plot.png)
![Zoomed](https://github.com/Berendei-Jr/CompareFace/blob/master/FAR-FRR/far-frr-plot-zoomed.png)
