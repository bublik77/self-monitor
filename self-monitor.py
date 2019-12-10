#!/usr/bin/env python2

import os
import sys

def chech_if_installed_vagrant():
    vagr="vagrant -v"
    return_value=os.system(vagr)

    if return_value != 0:
        #print("vagrant not installed")
        return False
        #try:
        #    os.system("apt -y install vagrant")
        #except:
        #    print("something goes wrong")

    else:
        #print("vagrant installed")
        return True

def install_vagrant():
    os.system("apt update && apt -y install vagrant")

if __name__=="__main__":
    if len(sys.argv) - 1 == 0:
        print("you need add some of argument")
        print("Example: init.py init")
        sys.exit(0)
        
    if sys.argv[1].lower() == "init":
        if not chech_if_installed_vagrant():
            install_vagrant()
        else:
            print("")

    elif sys.argv[1].lower() == "stop":
        if chech_if_installed_vagrant():
            os.system("vagrant halt")
        else:
            print("vagrant not installed")
    elif sys.argv[1].lower() == "start":
        if chech_if_installed_vagrant():
            os.system("vagrant up")
        else:
            print("vagrant not installed")
    elif sys.argv[1].lower() == "destroy":
        if chech_if_installed_vagrant():
            os.system("vagrant destroy")
        else:
            print("vagrant not installed")
    else:
        print("unknow urgument")
