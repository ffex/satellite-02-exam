# Esonero I

*Academic Year*: 2025/2026 Course: Artificial Intelligent Systems - Intelligent Model  

*Exemption Project*: Research in the state space.  

## Submission Requirements 

- Each group must present the implementation carried out within the AIMA Python of the following agent domains by Tuesday, May 5, 2025, during the lecture.  

- For each domain, example problems with initial state and objective of increasing difficulty must be provided.  

- Upon delivery, the teacher requests to prepare and test variants of the example problems, so that each person in the group has a variant to briefly show (max 10 minutes for each group, including PC connection: bad time management will influence the grade).  

- The problems must be solved with search algorithms, including an iterative deepening one and an A* after defining an appropriate heuristic, and the solutions compared. For A*, at least two suitable heuristics should be defined, and a heuristic combination (MAX) should be implemented (see the slides to find how this case works). 

- The scripts for launching the runs must be present in the code. 

- A short one-page printed report will be given to the professor when presenting, containing a comparison table between the different reproducible runs, reporting execution times and the number of nodes created/examined. A .zip file including the report and the code to be run during the lecture should be uploaded via Unistudium before the presentation (a proper submission form will be made available).

## Exercise - Satellite02 

- An artificial satellite can be in one of the 8 positions of a "compass rose" (N, NE, E, SE, S, SW, W, NW) and can move with the actions rotate left (RL) or rotate right (RR).  

- In various positions, various stars, planets, and galaxies can be found which can be photographed with the action TakePic(object) if the satellite is oriented in the position of the object and has a charge of at least 2.  

- Memory: The effect is that the memory space of the photo will be occupied (3 units of memory for each low-resolution SD photo, 10 for each high-resolution HD photo).  

- TakePic actions are not possible if there is not enough space in memory to contain the photos.  

- Memory can be freed with the action of sending (send) the photos to Earth, which requires being positioned at North (N) and costs 2; the send action sends only one photo at a time.  

- The memory can contain a maximum of two photos. 

- The RR and RL actions costs 1 each. 

### Example Problem
Given an initial state of initial charge and stellar objects in various directions, a final state with photos of stellar objects sent to Earth is required. 

# Installation guide
Make a tree directory like that:
```
../
├── aima-python
│   └── ...
└── satellite-02-exam
    ├── doc
    │   └── lezione_robot_TODO.ipynb
    ├── PE_IM_heuristics.py
    ├── PE_IM_problems.py
    ├── PE_IM_run.py
    ├── PE_IM_satellite.py
    ├── PE_IM_utils.py
    ├── README.md
    └── results.csv
```

To install aima-python use the installation  in the official repository [aima-python](https://github.com/aimacode/aima-python)
```
git clone https://github.com/aimacode/aima-python
```

To find the aima-python modules we have to tell to python to search also in another path. So in the `satellite-02-exam` directory we have to run:
```
export PYTHONPATH=$PYTHONPATH:$(pwd)/../aima-python
```

right now we have connected this repository with [aima-python](https://github.com/aimacode/aima-python) and we can do:

```
python3 PE_IM_run.py

```
