# Cooperative Evidential Semantic Grid

## Introduction
This project use the 2 dimenssional bounding boxes from cameras of road side units (RSU) and on-board units (OBU) to generate an semantic occupancy map of a scene. We focused our work on situations at intersection and especially at round-abouts. 

## installation

### APT
To compile and run the CPP libraries, you'ill need to install *opencv*. You will also need python 3.9. 
```bash
sudo apt update
sudo apt install libopencv-dev python3-opencv
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.9 python3.9-tk python3.9-distutils python3.9-venv
```

### Create and configure the venv
A Python 3.9 virtual environment is advised. Run the following command in the Source directory of the project.
```bash
python3.9 -m venv venv-project
source venv-project/bin/activate
pip install -r requirements.txt
``` 


### VSCODE Extession
- Makefile tools
- C/C++


## Run the code
*NB: For now, the code may only work on linux.* 

### Virtual environement
The project runs inside a virtual environement which is included in this repository. Run the following command to enter in the virtual environement.

```bash
source venv/bin/activate
```

### Using the scripts
<!-- TODO -->
This section will be updated as the project progresses.

### Entry point
<!-- TODO -->
The entry point of the project is the Sources/testbench.py script.

### Unit tests

## Documentation
Some documentation is available in the Sources/html folder. 