#!/usr/bin/env python3

import os
import sys
import subprocess

def check_if_installed_vagrant():
	try:
		returnCode = subprocess.call(["vagrant","--version"], stdout=subprocess.PIPE)
		if returnCode == 0:
			return True
	except:
		return False

def check_ansible_installed():
	try:
		returnCode = subprocess.call(["ansible","--version"], stdout=subprocess.PIPE)
		if returnCode == 0:
	 		return True
	except:
		return False

def install_vagrant():
	print("there is no vagrant and we are instaling it")
	osInst=""
	try:
		with open("/etc/os-release", 'r') as line:
			for i in line:
				if "ubuntu" in i:
					osInst="ubuntu"
				elif "centos" in i:
					osInst="centos"
	except Exception as ex:
		print(ex)

	if osInst == "ubuntu":
		os.system("sudo apt update && sudo apt -y install vagrant")
	elif osInst == "centos":
		print("Please donload vagrant from https://www.vagrantup.com/downloads.html and run this script agein")
		sys.exit()

def install_ansible():
	print("there is no ansible and we are instaling it")
	osInst=""
	addPpa="sudo apt-add-repository -y ppa:ansible/ansible"
	addepel="sudo yum install -y epel-release"
	installAnsC="sudo yum -y install ansible"
	installAns="sudo apt install -y ansible"
	try:
		with open("/etc/os-release", 'r') as line:
			for i in line:
				if "ubuntu" in i:
					osInst="ubuntu"
				elif "centos" in i:
					osInst="centos"
	except Exception as ex:
		print(ex)

	if osInst == "ubuntu":
		os.system(addPpa)
		os.system(installAns)
	elif osInst == "centos":
		os.system(addepel)
		os.system(installAnsC)

def creatVM():
	#print("I'm in create VM function")
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
	pathFile=os.getcwd() + "/" + "Vagrantfile"
	vgStatus = os.popen("vagrant status").read()
	if os.path.isfile(pathFile):
		if "poweroff" in vgStatus:
			return False
		elif "running" in vgStatus:
			return True
		elif "not created" in vgStatus:
			return "not created"
	else:
		return "there is no Vagrant file, please run script with init options"

# def initVagVM():
# 	if vmStatus():
# 		print("VM is running, try run script with another parametr")
# 		sys.exit()
# 	elif vmStatus() == False:
# 		print("VM is present but stoped, try run script with start or destroy parameter")
# 	elif vmStatus() == "not created":
# 		print("remove Vagrant file in the directory and run init again")
	
def run_ansible():
	invfile=os.getcwd() + "/" + "inv"
	playBookFile= os.getcwd() + "/" + "install_soft.yml"
	runCommand = "ansible-playbook -i {} {}".format(invfile,playBookFile)
	if os.path.isfile(invfile) and os.path.isfile(playBookFile):
		try:
			os.system(runCommand)
		except Exception as ex:
			print(ex)
	else:
		print("Please check if inventory or playbook yml file is present")


if __name__=="__main__":

	if len(sys.argv) - 1 == 0:
		print("you need add some of argument")
		print("Example: init.py init")
		sys.exit(0)
		
	if sys.argv[1].lower() == "init":
		if not check_if_installed_vagrant():
			install_vagrant()
			creatVM()
			if not check_ansible_installed():
				install_ansible()
		elif vmStatus() == "not created":
			print("It looks like the VM Vagrant file is present but VM not created, try to delete Vagrant file and start script againAAAAAAA")
			sys.exit()
		elif vmStatus() == False or vmStatus() == True:
			print("It looks like the VM is present, try to start or stop or delete it")
			sys.exit()
		else:
			if not check_ansible_installed():
				install_ansible()
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
