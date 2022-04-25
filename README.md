# Motion detection in UNT

[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://support.microsoft.com/ru-ru/windows) 
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com) 
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org) 
[![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)



- [Installation](#Installation)
- [Run](#Run)
- [Algorithm](#Algorithm)





<a name="Installation" />

## Installation

1. Open terminal and clone git repository. 

```python
git clone https://github.com/aktumar/DOP_human_detection.git
```

2. Create the virtual environment.

```python
virtualenv venv
```

3. Activate the virtual environment.

​	*Windows*

```python
venv\Scripts\activate
```

​	*Ubuntu/Linux*

```python
source venv/bin/activate
```

4. Run a requirements.txt file to install project’s dependencies

```python
pip install -r requirements.txt
```





<a name="Run" />

## Run

To see all the logs on the user interface, before running, you need to open [cutelog](https://github.com/busimus/cutelog) with the command:
```python
start cutelog
```
<p align="center">
    <img width="70%" src="https://github.com/aktumar/DOP_human_detection/blob/main/asset/Logging.png"/> 
</p>


To run program use following command:


1. Use your local camera. Write 'true' to run camera

```python
python run.py -c true
```

2. Use RTSP with given .ini file. Choose one computer(camera). 

   .ini file filling example: *rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101*

```ini
[10]
USERNAME = admin
PASSWORD = 12345
IP_ADDRESS = 192.168.1.210
PORT = 554
DIR = Streaming/Channels
COMPUTER = 101
```

```python
python run.py -u 10
```

3. Use local video path. Make sure that you have entered the correct directory for the video folder.

```python
python run.py -v 1.mp4
```





<a name="Algorithm" />

## Algorithm

Constantly using a neural network to recognize and monitor a person's actions in order to detect cheating in the UNT can be extremely laborious. To reduce server load, you can preprocess frames and send only specific parts of the frames for recognition. In this area, an examinee is typically singled out for performing certain actions that are different from the standard state. The following is a description of this algorithm: 

1. The frame's parts that differ from the previous one are identified. 
2. These areas are highlighted by boxes and include both significant and minor changes. As a result, you can eliminate even the tiniest details at this stage. 
3. When we have a lot of boxes, we can classify them by determining the coordinates of their neighbors. At this point, each of the box's four corners is involved. The window's parameters are used to determine the maximum distance between neighboring points. 
4. Once the boxes have been classified, each cluster is merged into a single box. 
5. However, it is worth considering that most of the frames contain third-party movements, such as a passerby or another examiner in the background. This is accomplished by selecting the largest box in terms of area.

<p align="center">
    <img width="70%" src="https://github.com/aktumar/DOP_human_detection/blob/main/asset/Animation.gif"/> 
</p>

