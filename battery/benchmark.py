#!/bin/env python3

import json
import time
import argparse
import mysql.connector
import subprocess
import signal
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument("--info",action="count",help="gather and display battery info")
parser.add_argument("--quick", action="count",help="Run a quick battery tests")
parser.add_argument("--monitor",action="count",help="Monitor battery in 5 second intervals")
parser.add_argument("--test",help="Run selected test")


args = parser.parse_args()

def sys_file(root, file):
   
    output = subprocess.run(
                ["cat",root+file],
                capture_output=True,
                text=True
                ).stdout.split("\n")[0]
    return output

def battery():
    rootdir = "/sys/class/power_supply/BAT0/"
    info = {}
    info["status"] = sys_file(rootdir,"status")
    info["percent"] = sys_file(rootdir,"capacity")
    #info["capacity_level"] = sys_file(rootdir,"capacity_level")
    info["charge_full"] = sys_file(rootdir,"charge_full")
    info["charge_now"] = sys_file(rootdir,"charge_now")
    info["current_now"] = sys_file(rootdir,"current_now")
    return info

def power_profile():
    info = {}
    
    if os.path.exists("/usr/bin/system76-power"):
        #print("found system76-power")
        info["graphics"] = subprocess.run(["system76-power","graphics"],capture_output=True,text=True).stdout.split("\n")[0]
        
    bmax = sys_file("/sys/class/backlight/acpi_video0/","max_brightness")
    bcurrent = sys_file("/sys/class/backlight/acpi_video0/","brightness")
    info["backlight"] = {
                         "max":float(bmax),
                         "current":float(bcurrent),
                         "precent":float(bcurrent)/float(bmax)
                        }
        
    return info
    

def gather_info(infoType):
    print("\n")
    match infoType:
       case "all":
            bat = battery()
            print("Battery Info:")
            for key in bat.keys():
                print("  ",key,":",bat[key])
            print("\nPower Profile:")
            pp = power_profile()
            for key in pp:
                print("  ",key,":",pp[key])
    print("\n")    

if args.quick:
    print("Running quick battery tests")
    
if args.info:
    gather_info("all")
    
if args.monitor:
    while 1:
        gather_info("all")
        time.sleep(5)
        os.system('clear')
        
if args.test:
    if os.path.exists(args.test):
        print(args.test)
