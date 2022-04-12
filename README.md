# Motion detection in UNT

![Windows Badge](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)![Windows Badge](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)



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

```
python RTSP.py -c ON
```

2. Use RTSP with given .ini file. Choose one computer(camera)

```
python RTSP.py -u 151
```

3. Use local video path.

```
python RTSP.py -v 1.mp4
```

