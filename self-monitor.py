#!/usr/bin/env python3

import os
import sys

def check_if_installed_vagrant():
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
def check_ansible_installed():
	ans="ansible --version"
	return_value=os.system(ans)
	if return_value == 0:
		return True
	else:
		return False

def install_vagrant():
	try:
		os.system("sudo apt update && sudo apt -y install vagrant")
	except:
		print("fail")

def install_ansible():
addPpa="sudo apt-add-repository -y ppa:ansible/ansible"
installAns="sudo apt install ansible"
try:
	os.system(addPpa)
	os.system(installAns)		
except Exception as ex:
	print(ex)

	
def creatVM():

	print("I in create VM function")
	lineIndex=0
	osSelect=input("enter VM OS to create centos or ubuntu: ")
	osVersion=input("enter OS selected version : ")
	pathFile=os.getcwd() + "/" + "Vagrantfile"
	vgFileOption="  config.vm.network \"forwarded_port\", guest: 443, host: 443, auto_correct: true\n  config.vm.network \"private_network\", ip: \"172.16.0.20\", virtualbox__intnet: true\n" 
	createVgVm="vagrant init -m {}/{}".format(osSelect,osVersion)
	try:
		os.system(createVgVm)
	except Exception as ex:
		print(ex)
		sys.exit()
	
	with open(pathFile, 'r') as vgFileR: 
		content=vgFileR.readlines() 
		for index, line in enumerate(content): 
			if line.startswith("end"): 
				lineIndex=index
	content.insert(lineIndex,vgFileOption)
	with open(pathFile, 'w') as vgFileW: 
		vgFileW.writelines(content)
	try:
		os.system("vagrant up")
	except Exception as ex:
		print(ex)
		sys.exit()    

def vmStatus():
	#vmVagStatusOff="vagrant status | grep -o poweroff"
	#vmVagStatusOn="vagrant status | grep -o running""
	#vmVagStatusPresent="vagrant status | grep -o "not created" | head -1"
	pathFile=os.getcwd() + "/" + "Vagrantfile" 
	if os.path.isfile(pathFile):
		if os.system("vagrant status | grep -o poweroff") == 0:
			return False
		elif os.system("vagrant status | grep -o running") == 0:
			return True
		elif os.system("vagrant status | grep -o 'not created' | head -1") == 0:
			return "not created"
	else:
		return "no vm"

def initVagVM():
	if vmStatus():
		print("VM is running, try run script with another parametr")
		sys.exit()
	elif vmStatus() == False:
		print("VM is present but stoped, try run script with start or destroy parameter")
	elif vmStatus() == "not created":
		print("remove Vagrant file in the directory and run init again")
	


if __name__=="__main__":

	if len(sys.argv) - 1 == 0:
		print("you need add some of argument")
		print("Example: init.py init")
		sys.exit(0)
		
	if sys.argv[1].lower() == "init":
		if not check_if_installed_vagrant():
			install_vagrant()
			creatVM()
		elif vmStatus() == "not created":
			print("It looks like the VM Vagrant file is present but VM not created, try to delete Vagrant file and start script againAAAAAAA")
			sys.exit()
		elif vmStatus() == False or vmStatus() == True:
			print("It looks like the VM is present, try to start or stop or delete it")
			sys.exit()
		else:
			creatVM()
	elif sys.argv[1].lower() == "stop":
		if check_if_installed_vagrant():
			os.system("vagrant halt")
		else:
			print("vagrant not installed")
	elif sys.argv[1].lower() == "start":
		if check_if_installed_vagrant():
			os.system("vagrant up")
		else:
			print("vagrant not installed")
	elif sys.argv[1].lower() == "destroy":
		if check_if_installed_vagrant():
			os.system("vagrant destroy")
			if os.path.exists(os.getcwd() + "/" + "Vagrantfile"):
				os.remove(os.getcwd() + "/" + "Vagrantfile")
		else:
			print("vagrant not installed")
	else:
		print("unknow urgument")
