import os
import shutil

# Create path
def create_path(a, *p):
    return os.path.join(a, *p)

# Create a new directory
def create_dir(dir_name):
    try:
        os.mkdir(dir_name)
        print("Directory " , dir_name ,  " Created ") 
    except FileExistsError:
        print("Directory " , dir_name ,  " already exists")
        
# Delete a directory
def delete_dir(dir_name):
    try:
        shutil.rmtree(dir_name)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        
# Delete a file
def delete_file(file_path):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except FileExistsError:
        print("File not found in the path")

# Copy file
def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

# Move single file    
def move_file(src, dst):
    try:
        shutil.move(src, dst)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        
# Move contents
def move_contents(src, dst):
    try:
        file_names = os.listdir(src)
        for file_name in file_names:
            source_file = create_path(src, file_name)
            shutil.move(source_file, dst)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        
# Give script permission
def give_permission(file_path):
    try:
        os.chmod(file_path, 755)
    except OSError as e:
        print(f'Error: can not give permision for {file_path}')
        
# Compile with protoc
def proto_compile(base_ref, proto_path, proto_files):
    try:
        os.system(f'cd {base_ref} && {proto_path} {proto_files} --python_out=.')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))        

# Install Pip Package
def pip_install(package):
    try:
        os.system(f'python -m pip install {package}')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        
# Execute script
def execute_script(script):
    try:
        os.system(f'python {script}')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        
# Execute make
def execute_make(make_script, base_ref=None):
    try:
        if base_ref:
            os.system(f'cd {base_ref} && make {make_script}')
        else:
            os.system(f'make {make_script}')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
        