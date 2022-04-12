# Motion detection in UNT

[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://support.microsoft.com/ru-ru/windows) [![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com) [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org) [![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org)



- [Installation](#Installation)
- [Run](#Run)





<a name="Installation" />

## Installation

```python
# склонируйте гит файл
git clone https://github.com/aktumar/DOP_human_detection.git


```



<a name="Run" />

## Run

To run program use following command:

```python
# Use your local camera. Write ON to run camera
python RTSP.py -c ON

# Use RTSP with given .ini file. Choose one computer(camera)
python RTSP.py -u 151

# Use local video path.
python RTSP.py -v 1.mp4
```

