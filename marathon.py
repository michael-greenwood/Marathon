# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 14:57:11 2019

@author: mgreenwo
Copywrite 2016 Government of Canada

"""

import os
import json
import time
import subprocess
sleep_time = 60*30 #check every 10 minutes

job_list = []
runs = []


target_location = "username@IP:targetdirectory" # should include username@IP:targetdirectory

class job_run():
    fname = ""
    directory = ""
    
    def __init__(self,fname):
        self.fname = fname
        self.directory = "./"+fname+"/"
        self.restart_list = []
        self.zip_files=[]
        self.sent_files = []
    def check_for_new_files(self):
        #update the restart_list
        if(os.path.exists(self.directory)):
            for file in os.listdir(self.directory):
                if file.startswith("restart_"):
                    if not(file in self.restart_list):
                        self.restart_list.append(file)
                        self.zip_files.append(0)
                        self.sent_files.append(0)
    def load_data(self):
        file_r = "./run_data/"+self.fname+"_restart.json"
        file_z = "./run_data/"+self.fname+"_zip.json"
        file_s = "./run_data/"+self.fname+"_sent.json"
        if(os.path.exists(file_r)):
            fr = open(file_r,'r')
            self.restart_list = json.load(fr)
            fr.close()
        if(os.path.exists(file_z)):
            fz = open(file_z,'r')
            self.zip_files = json.load(fz)
            fz.close()
        if(os.path.exists(file_s)):
            fs = open(file_s,'r')
            self.sent_files = json.load(fs)
            fs.close()
        
    def save_data(self):
        file_r = "./run_data/"+self.fname+"_restart.json"
        file_z = "./run_data/"+self.fname+"_zip.json"
        file_s = "./run_data/"+self.fname+"_sent.json"
        fr = open(file_r,'w')
        fz = open(file_z,'w')
        fs = open(file_s,'w')

        json.dump(self.restart_list,fr)
        json.dump(self.zip_files,fz)
        json.dump(self.sent_files,fs)
        fr.close()
        fz.close()
        fs.close()
    def Zip_new_files(self):
        for i in range(len(self.zip_files)):
            if(self.zip_files[i] == 0):
                command = "tar -czvf "+self.directory+self.fname+"_"+self.restart_list[i]+".tar.gz "+ self.directory+self.restart_list[i]
                print(command)
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                (stdout,stderr)=process.communicate()
                self.zip_files[i] = 1
    def Send_new_files(self):
        for i in range(len(self.sent_files)):
            if(self.sent_files[i] == 0):
                command = "scp "+ self.directory+self.fname+"_"+self.restart_list[i]+".tar.gz "+ target_location
                print(command)
                process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                (stdout, stderr) = process.communicate()
                self.sent_files[i] = 1

def Check_for_new_files(runs):
    for r in runs:
        r.check_for_new_files()
def Zip_new_files(runs):
    for r in runs:
        r.Zip_new_files()
def Send_new_files(runs):
    for r in runs:
        r.Send_new_files()
def Save_data(runs):
    for r in runs:
        r.save_data()
        
def Update_job_list():
    file = open("jobnames.txt", "r") 
    for f in file:
        #strip white space and end of line characters
        fname = (f.strip('\n')).strip()
        fname_out = fname.replace('/','_')
        print(fname_out)
        if not (fname in job_list):
            print("new run added : adding "+fname+" to list")
            job_list.append(fname)
            j = job_run(fname)
            j.load_data()
            runs.append(j)
    #check if already in job_list
    file.close()
    
if __name__ == "__main__":
    while(1):
        print("checking Files")
        Update_job_list()
        Check_for_new_files(runs)
        Zip_new_files(runs)
        Send_new_files(runs)
        Save_data(runs)
        time.sleep(sleep_time)


                
