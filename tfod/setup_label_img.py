from  urllib.request import urlretrieve

import zipfile
import os_commands

# Preset
# print('Creating folder')
label_img_path = os_commands.create_path('..', 'labelimg')
os_commands.create_dir(label_img_path)

# Download
print('Downloading repo')
url = 'https://github.com/tzutalin/labelImg/archive/refs/heads/master.zip'
label_img_project_path = os_commands.create_path(label_img_path, 'labelimg.zip')
urlretrieve(url, label_img_project_path)

print('Extracting repo zip')
with zipfile.ZipFile(label_img_project_path, 'r') as zip_ref:
    zip_ref.extractall(label_img_path)
os_commands.delete_file(label_img_project_path)
from_path = os_commands.create_path(label_img_path, f'labelimg-master')
os_commands.move_contents(from_path, label_img_path)

# Install
os_commands.pip_install('pyqt5')
os_commands.pip_install('lxml')

os_commands.execute_make(
    'qt5py3',
    base_ref=label_img_path
)

print('You can run "python labelimg/labelImg.py" to open the software')