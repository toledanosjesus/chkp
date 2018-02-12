#!/usr/bin/env python

import requests
import json
import colors
import re
import urllib
import os

from urllib3.exceptions import InsecureRequestWarning

#____VARIABLES_TO_CHANGE_________
#################################
user="[user]"					#
password="[password]"			#
MGMT_IP="[Management_IP]"		#
port="443"						#
Policy_name="Standard"			#
Layer_name="Network"			#
#################################

# Function to create the Title
def title(name):
  os.system('clear')
  print colors.BIYellow + '\n#####################################################'
  print '#                  R80.10 API                       #'
  print '#               '+name+'                  #'
  print '#####################################################' + colors.Color_Off

# Function to execute a command
def api_call(login_data, command, json_payload):
    url = 'https://' + login_data["mgmtip"] + ':' + login_data["port"] + '/web_api/' + command
    if login_data["sid"] == '':
        request_headers = {'Content-Type' : 'application/json'}
    else:
        request_headers = {'Content-Type' : 'application/json', 'X-chkp-sid' : login_data["sid"]}
    r = requests.post(url,data=json.dumps(json_payload), headers=request_headers, verify=False)
    # print r.text
    return r.json()

def show_group(login_data,name_group):
	group_data = {'name':name_group}
	show_group = api_call(login_data,'show-group', group_data)
	# print(json.dumps(show_group))
	return show_group

# Function to login into the API server
def login(login_data):
	printlog("Login into the server...")
	payload = {'user':login_data["user"], 'password' : login_data["pw"], 'continue-last-session':'true'}
	response = api_call(login_data, 'login', payload)
	printlog("API:\tLogin DONE!")
	printlog("API:\tYour session ID is: "+response["sid"])
	return response["sid"]

# Function to add new host
def add_host(login_data,IPs,name_group):
	for unique_ip in IPs:
		new_host_data={'name':unique_ip, 'ip-address':unique_ip, 'comments':'This is a TOR node.','tags':'TOR'}
		new_host = api_call(login_data,'add-host', new_host_data)
		# print(json.dumps(new_host))
		printlog("API:\tHost "+unique_ip+" succesfully added.")
		add_host_to_group(login_data,unique_ip,name_group)

# Function to add a group 
def add_group(login_data,name_group=None):
	if name_group == None:
		name_group = "TOR_Group"
	group_data = {'name': name_group }
   	group = api_call(login_data,'add-group',group_data)
	printlog("API:\tGroup "+name_group+" succesfully added.")
   	return name_group
   	# print json.dumps(group)

# Function to add host to a group
def add_host_to_group(login_data,host,group):
	add_host_group_data = {'name':host, 'groups':group}
	add_host_group = api_call(login_data,'set-host',add_host_group_data)
	printlog("API:\tHost "+host+" succesfully added to the group "+group+".")
   	# print(json.dumps(add_host_group))

# Function to remove hosts
def del_host(login_data,names,name_group):
	for unique_name in names:
		#del_host_from_group(login_data,unique_name,name_group)
		del_host_data={'name':unique_name}
		del_host = api_call(login_data,'delete-host', del_host_data)
		# print(json.dumps(del_host))
		printlog("API:\tHost "+unique_name+" succesfully deleted.")

# Function to set the members of a group
def set_members_group(login_data,hosts,group):
	members_group_data = {'name':group,'members':hosts}
	del_host_group = api_call(login_data,'set-group',members_group_data)
	printlog("API:\tHosts "+str(hosts)+" succesfully joined the group "+group+".")
   	# print(json.dumps(del_host_group))

# Function to publish the policy
def publish_policy(login_data):
	next("The policy changes will be publish, push ENTER to continue...\n")
	publish = api_call(login_data,"publish", {})
	print "publish result: " + json.dumps(publish)

# Function to logout
def logout(login_data):
	logout_result = api_call(login_data,"logout", {})
	# print "logout result: " + json.dumps(logout_result)
	print "\nLogout result:\t" + logout_result["message"]

# Function to show information about the current status
def printlog(message=None):
    if message is None:
        message="R80.10 API is currently working...\n"
    print message + "\n"

# Function to continue with the program
def next(message=None):
    if message is None:
        message="Push ENTER to continue...\n"
    raw_input("\n"+message+"\n")

# Function to say Good Bye!
def end():
    print("\n\nSee you soon!")
    message="Push ENTER to exit..."
    next(message)

# Function to the the current IP's address of the TOR nodes
def get_TOR_Nodes():
	TOR_Nodes = []
	listIP = urllib.urlopen('https://check.torproject.org/cgi-bin/TorBulkExitList.py?ip=1.1.1.1')
	for ip in listIP:
	    ip = ip.strip()
	    if re.match('\d+(\.\d+){3}$', ip):
	        TOR_Nodes.append(ip)
	listIP.close()
	return TOR_Nodes

# Function to compare the new IP's addresses list with the old one 
def compare_list(new_list,login_data,name_group):
	old_file="TOR_old_IP_list.txt"
	new_file="TOR_new_IP_list.txt"

	old_list=[]		# IP list with the previous addresses
	to_keep=[]		# List of IP's to keep
	to_delete=[]	# List of old IP's to delete
	to_add=[]		# List of new IP's to add

	k=0		# Number of IP's to keep
	d=0		# Number of old IP's to delete
	a=0		# Number of new IP's to add

	changes = 0		# Variable to see if there is any changes to apply

	with open(old_file,'r') as ip_list: # Create a list with the old IP's
		for i in ip_list:
			i = i.strip()
			old_list.append(i)

	for old_ip in old_list:		# Compare what old IP's will be kept ore deleted
		if old_ip in new_list:
			k+=1
			to_keep.append(old_ip)
		else:
			d+=1
			to_delete.append(old_ip)

	for new_ip in new_list:		# Compare which one are the new IP's
		if new_ip not in old_list:
			a+=1
			to_add.append(new_ip)

	if a != 0:
		add_host(login_data,to_add,name_group)	# Add the new hosts

	if a != 0 or d!=0:					# Set TOR_Group members again in case of any change
		changes = 1
		members=to_add+to_keep
		set_members_group(login_data,members,name_group)	

	if d != 0:								
		del_host(login_data,to_delete,name_group)	# Del the old hosts

	if changes == 1:
		with open(old_file,'w') as ip_list:			# Rewrite the file with the new IP's list 
			for i in new_list:
				ip_list.write(i+"\n")

	return changes

# Main Function
def main(login_data):
	requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

  	title("     PROGRAM      ")

	sid=login(login_data)
	login_data["sid"]=sid

	name_group="TOR_Group"
	check_group=show_group(login_data,name_group)	# Check if the group TOR_Group exists

	if "code" in check_group:
		print colors.On_IRed + "WARNING!"
		print colors.IRed + "The group TOR_Group did not exist and will be created.\n" + colors.Color_Off
		check_group = 1
		add_group(login_data)

	TOR_Nodes=get_TOR_Nodes()

	check_updates=compare_list(TOR_Nodes,login_data,name_group)
	if check_updates == 1 or check_group == 1:
		publish_policy(login_data)
	else:
		printlog("\nThere's NOT any changes. Proceeding to login out of the system.")

	logout(login_data)
	end()
	os.system('clear')

login_data = {'user':user,'pw':password, 'mgmtip':MGMT_IP, 'port':port,'policy':Policy_name,'layer':Layer_name,'sid':''}

main(login_data)