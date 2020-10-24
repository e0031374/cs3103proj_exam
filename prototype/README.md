# Prototype: Exam Test Facility
### I want to conduct an exam and not let my students cheat so all their packets belongs to me

## Setup Instructions
To run, please follow the following instructions to set up the proper environment

### Setup Virtual Environment for Python
1. `$ python3 -m venv venv`
1. `$ source venv/bin/activate`

### Install python module dependencies in Virtual Env
1. `(venv) $ sudo apt-get install python3-tk`

1. `(venv) $ pip install pandas` 
1. `(venv) $ pip install xlrd`
1. `(venv) $ pip install xlsxwriter`

1. `(venv) $ pip install scapy`
1. `(venv) $ pip install elevate`

### Run Exam Program
1. `(venv) $ python main.py`

### Exit Virtual Env
1. `(venv) $ deactivate`


## File Listing
1. main.py : exam program
1. sample_questions.xlsx : questions for the exam and timer configuration
1. Answers.xlsx : program generated answers that student has provided for the exam
1. banana.pcap : packet captured for the duration of the exam
