import os_commands

def is_valid_option(option):
    return option == "y" or option == "n"

option = None
while not is_valid_option(option):
    option = input("Do you want to setup project folders? (y/n) ").lower()
    if option == "y":
        os_commands.execute_script('setup_folders.py')
    elif option == "n":
        print('Creation folders step skipped')
    
option = None
while not is_valid_option(option):
    option = input("Do you want to setup protoc? (y/n) ").lower()
    if option == "y":
        os_commands.execute_script('setup_protoc.py')        
    elif option == "n":
        print('Setup protoc step skipped')
        
option = None
while not is_valid_option(option):
    option = input("Do you want to setup Tensorflow Object Detection API? (y/n) ").lower()
    if option == "y":
        os_commands.execute_script('setup_tfod.py')
    elif option == "n":
        print('Setup Tensorflow Object Detection API step skipped')
        
option = None
while not is_valid_option(option):
    option = input("Do you want to setup LabelImg? (y/n) ").lower()
    if option == "y":
        os_commands.execute_script('setup_label_img.py')
    elif option == "n":
        print('Setup LabelImg step skipped')