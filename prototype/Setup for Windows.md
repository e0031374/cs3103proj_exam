## Setup Instructions (using Anaconda)
Download Anaconda from https://www.anaconda.com/, then follow the following instructions to set up the proper environment

### Setup Virtual Environment for Python
1. Open Anaconda Prompt
1. `conda create --name venv`
1. `conda activate venv`

### Install python module dependencies in Virtual Env
1. `conda install -c anaconda tk`
1. `conda install -c anaconda pandas` 
1. `conda install -c anaconda xlrd`
1. `conda install -c anaconda xlsxwriter`

1. `pip install scapy`
1. `pip install elevate`

### Run Exam Program
1. Run Anaconda prompt as Administrator
1. `conda activate venv`
1. `python main.py`

### Exit Virtual Env
1. `conda deactivate`


## File Listing
1. main.py : exam program
1. sample_questions.xlsx : questions for the exam and configuration for timer
1. Answers.xlsx : program generated answers that student has provided for the exam
1. banana.pcap : packet captured for the duration of the exam
