# Motion detection in UNT

[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://support.microsoft.com/ru-ru/windows) [![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com) [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org) [![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)



- [Installation](#Installation)
- [Run](#Run)





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

To run program use following command:

1. Use your local camera. Write ON to run camera

```python
python RTSP.py -c ON
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
python RTSP.py -u 10
```

3. Use local video path. Make sure that you have entered the correct directory for the video folder.

```python
python RTSP.py -v 1.mp4
```

