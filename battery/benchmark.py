#!/bin/env python3

import json
import time
import argparse
import subprocess
import signal
import sys
import os

parser = argparse.ArgumentParser()
parser.add_argument("--info",action="count",help="Gather and display battery info")
parser.add_argument("--quick", action="count",help="Run a quick battery test")
parser.add_argument("--full", action = "count",help="Run comprehensive battery test")
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
    
   # bmax = sys_file("/sys/class/backlight/acpi_video0/","max_brightness")
  #  bcurrent = sys_file("/sys/class/backlight/acpi_video0/","brightness")
   # info["backlight"] = {
   #                      "max":float(bmax),
    #                     "current":float(bcurrent),
    #                     "precent":float(bcurrent)/float(bmax)
     #                   }
        
    return info

def switch_power_profile(mode):
    if os.path.exists("/usr/bin/system76-power"):
        output = subprocess.run(["system76-power","profile",mode],capture_output=True,
                text=True
                ).stdout.split("\n")[0]
        return output

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


def run_app(app):
   
    output = subprocess.Popen(
                app
                )
    return output
    
def set_backlight(level):
    root = "/sys/class/backlight/"
    blmax = 100
    blmin = 1
    if os.path.exists(root+"intel_backlight"):
        root = root+"intel_backlight/"
    if os.path.exists(root+"amdgpu_bl0"):
        root = root+"amdgpu_bl0/"
        
    blmax = sys_file(root,"max_brightness")
    set_level = level * float(blmax)
    output = subprocess.run(
               ["echo "+str(int(set_level))+" | sudo tee "+root+"brightness"],
                capture_output=True,
                shell=True,
               text=True
               ).stdout.split("\n")[0]
        
    
    
def run_test(name,duration,apps,backlight):

    begin = {}
    end = {}
    #os.system("clear") 
    print("Running test",name)
    print("  Backlight =", backlight)
    print("  Durtation =", duration,"minutes")
    set_backlight(backlight)
    for a in apps:
        print("  Launching",a)
        run_app(a)
    
    gather_info("all")
    begin = battery()
    time.sleep(duration*60)
    end = battery()
    #gather_info("all")
    battery_loss = float(begin["charge_now"]) - float(end["charge_now"])
    battery_life = float(duration) * (float(begin["charge_full"]) / battery_loss) 
    print("\nTest complete")
    print("Percent battery loss in",duration,"minutes is:",float(begin["percent"]) - float(end["percent"]),"%")
    print("estimated battery life:","{:.2f}".format(battery_life),"minutes -or-","{:.2f}".format(battery_life/60))

if args.quick:
    print("Running quick battery tests")
   # gather_info("all")
    print("\n")
    switch_power_profile("battery")
    run_test("battery profile",2,[],0.5)
    time.sleep(10)
    print("\n")
    switch_power_profile("balanced")
    run_test("balanced profile",2,[],0.5)
    time.sleep(10)
    print("\n")
    switch_power_profile("performance")
    run_test("performance profile",2,[],0.5)
    
    
if args.info:
    gather_info("all")
    
if args.monitor:
    while 1:
        gather_info("all")
        time.sleep(5)
        os.system('clear')
        
if args.test:
    name = "unknown"
    duration = 10
    apps = []
    backlight = 0.5

    
    if os.path.exists(args.test):
        test = open(args.test,"r")
        test_settings = json.loads(test.read())
        test.close()
        if "duration" in test_settings.keys():
            duration = test_settings["duration"]
        if "apps" in test_settings.keys():
            apps = test_settings["apps"]
        if "backlight" in test_settings.keys():
            backlight = test_settings["backlight"]
        if "name" in test_settings.keys():
            name = test_settings["name"]
        if "apps" in test_settings.keys():
            apps = test_settings["apps"]
 
    run_test(name,duration,apps,backlight)
