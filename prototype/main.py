import time
import tkinter as tk
import pandas as pd
from tkinter import filedialog
import threading

# Dependencies for Pkt Cap
import os
from elevate import elevate     #scapy requires elevated privileges
from scapy.all import sr1, IP, ICMP, ARP, TCP, sniff 
from scapy.utils import PcapWriter

import pyscreenshot
import datetime

# Packet Capture Module
pktdump = PcapWriter("banana.pcap", append=True, sync=True)
elevate(graphical=False)

def monitor_callback(pkt):
    pktdump.write(pkt)
    #if TCP in pkt: # and pkt[TCP].op in (1,2): #who-has or is-at
    #    pktdump.write(pkt)
    #    pkt.show()
    #    return pkt.sprintf("%TCP.hwsrc% %TCP.psrc%")

def monitor_fn(t_out=10):
    #sniff(prn=monitor_callback, filter="tcp", store=0, timeout=t_out)
    sniff(prn=monitor_callback, store=0, timeout=t_out)

def monitor_wrapper(exam_duration):
    monitor_fn(exam_duration)
    
def screenshotFunc(interval):
    imageCount = 0;
    
    while True:
        # Capture screenshot
        image = pyscreenshot.grab()

        # Display captured screenshot
        # image.show();
        
        # Create folder for screenshots
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        
        # Save screenshot
        imageName = 'image%d' % imageCount
        image.save('screenshots/%s.png' % imageName)
        imageCount += 1
        time.sleep(interval)

class Main:
    """
    Handles input and CLI.
    """
    # Thread that signals an event when the time is up and/or student 
    # finished exam.
    global exam_ended
    exam_ended = threading.Event()

    
    def read_file(self):
        """
        Reads questions from the file provided.

        Returns pandas dataframe.
        """
        # Gets the filepath of the excel file
        root = tk.Tk()
        filepath = filedialog.askopenfilename()
        root.withdraw()
        
        # Reads the excel file
        xls = pd.ExcelFile(filepath)
        data = xls.parse(0)
        config = xls.parse(1)
        return data, config
    
    def parse(self, row):
        """
        Parses a row into a question with appropriate format.

        row : A row from pandas dataframe

        Returns a string of the question in the correct format.
        """
        s = str(row.iloc[0]) + '. ' + str(row.iloc[2]) + '\n'
        if str(row.iloc[1]).strip().upper() == 'MCQ':
            numbering = ord('A')
            i = 3
            while i < len(row):
                s += '\t' + chr(numbering) + ') ' + str(row.iloc[i]) + '\n'
                numbering += 1
                i += 1
        return s
    
    def store_ans(self, qns_num, ans, ans_dict):
        """
        Appends the answer to a dictionary.

        qns_num : An int denoting the question number.
        ans : A string denoting the answer.
        ans_dict : A dictionary containing all answers.

        Returns the answer dictionary.
        """
        ans_dict["Question"].append(qns_num)
        ans_dict["Answer"].append(ans)
        return ans_dict
    
    def write_file(self, ans_dict):
        """
        Writes the answers into an excel sheet and saves it.

        ans_dict : A dictionary containing the answers.
        """
        df = pd.DataFrame(ans_dict)
        writer = pd.ExcelWriter("Answers.xlsx", engine='xlsxwriter')
        df.to_excel(writer, index=False)
        writer.save()
        
    def initialise(self):
        """
        Initialises the program.
        
        Returns two pandas dataframes, the first one contains all questions 
        and the second one contains all configurations.
        """
        print(' EXAM SYSTEM '.center(80, '='))
        print('During this exam please note that all internet ports will be monitored. ')
        print('The program will also be taking screenshots at fixed intervals.')
        print()
        input('Press any key to continue')
        print('Please select an excel file')
        data, config = self.read_file()
        print('File uploaded successfully')
        print()
        print('Note that a timer will start once the exam begins. When the time is up, ' + 
              'your answers will be saved and the program will close automatically.')
        return data, config
    
    def timer(self, exam_duration):
        """
        Times the exam and ends it when time is up.
        
        config : A pandas dataframe containing the duration of the exam.
        """
        global exam_ended
        time.sleep(exam_duration)
        exam_ended.set()
    
    def program_loop(self, data):
        """
        Runs the main program loop.
        
        data :A pandas dataframe containing all the questions.
        """
        global exam_ended, ans_dict
        i = 0
        num_rows = len(data.count(axis='columns'))
        while 1:
            print(self.parse(data.iloc[i]))
            user_input = input('Answer: ').strip().upper()
            
            # Checks if input is valid
            while user_input < 'A' or user_input > 'Z' \
                or len(user_input) != 1 or user_input.isalpha() == False:
                print('Invalid input. Please input a character.')
                user_input = input('Answer: ').strip().upper()
            
            self.store_ans(i + 1, user_input, ans_dict)
            
            i += 1
            if num_rows == i:
                break
            
        exam_ended.set()
        
    def main(self):
        """
        The main method.
        """
        global exam_ended, ans_dict
        ans_dict = {}
        data, config = self.initialise()
        ans_dict['Question'] = []
        ans_dict['Answer'] = []
        exam_duration = int(config.iat[0, 0])
        interval = int(config.iat[0, 1])
        print('You will have %d minutes to complete the exam.' % (exam_duration / 60))
        input('Press any key to start the exam')
        print()
        
        t1 = threading.Thread(target=self.timer, args=[exam_duration], daemon=True)
        t2 = threading.Thread(target=monitor_wrapper, args=[exam_duration], daemon=True)
        t3 = threading.Thread(target=self.program_loop, args=[data], daemon=True)
        t4 = threading.Thread(target=screenshotFunc, args=[interval], daemon=True)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        
        # Wait for the exam to end before continuing
        exam_ended.wait()
        
        print(' END OF EXAM '.center(80, '='))
        self.write_file(ans_dict)
        return 
        
    
m = Main()
m.main()
