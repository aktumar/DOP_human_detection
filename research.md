# Scientific Research on Human detection in UNT (UNIFIED NATIONAL TESTING)

### RTSP - Real time streaming protocol

Большинство IP-камер поддерживает протокол потоковой передачи в реальном времени (RTSP) для управления потоковой 
передачей аудио и видео. Мы пытаемся использовать захват потока RTSP с IP-камеры с использованием OpenCV и Python.

OpenCV предоставляет класс VideoCapture, который позволяет захватывать видео из видеофайлов, последовательностей 
изображений, веб-камер, IP-камер и т. д. Чтобы захватить поток RTSP с IP-камеры, нам нужно указать URL-адрес RTSP в 
качестве аргумента. Поскольку URL-адрес RTSP не стандартизирован, разные производители IP-камер могут использовать 
разные URL-адреса RTSP. Многие производители предоставляют URL-адрес RTSP на своем веб-сайте или в руководстве 
пользователя. URL-адрес RTSP обычно состоит из имени пользователя, пароля, IP-адреса камеры, номера порта (554 — номер 
порта RTSP по умолчанию), имени потока.


Constantly using a neural network to recognize and monitor a person's actions in order to detect cheating in the UNT 
can be extremely laborious. To reduce server load, you can preprocess frames and send only specific parts of the frames 
for recognition. In this area, an examinee is typically singled out for performing certain actions that are different 
from the standard state. The following is a description of this algorithm: 

1. The frame's parts that differ from the previous one are identified. 
2. These areas are highlighted by boxes and include both significant and minor changes. As a result, you can eliminate 
even the tiniest details at this stage. 
3. When we have a lot of boxes, we can classify them by determining the coordinates of their neighbors. At this point, 
each of the box's four corners is involved. The window's parameters are used to determine the maximum distance between 
neighboring points. 
4. Once the boxes have been classified, each cluster is merged into a single box. 
5. However, it is worth considering that most of the frames contain third-party movements, such as a passerby or 
another examiner in the background. This is accomplished by selecting the largest box in terms of area.