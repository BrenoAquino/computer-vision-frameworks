from  urllib.request import urlretrieve

import _paths as paths

import zipfile
import os_commands

# Download
os_commands.create_dir(paths.models)
print('We will use the last version in master to download')
print('You can see the project in https://github.com/tensorflow/models')

print('Downloading repo')
url = 'https://github.com/tensorflow/models/archive/refs/heads/master.zip'
tfod_project_path = os_commands.create_path(paths.models, 'models.zip')
urlretrieve(url, tfod_project_path)

print('Extracting repo zip')
with zipfile.ZipFile(tfod_project_path, 'r') as zip_ref:
    zip_ref.extractall(paths.models)
os_commands.delete_file(tfod_project_path)
from_path = os_commands.create_path(paths.models, f'models-master')
os_commands.move_contents(from_path, paths.models)

# Install
print('Compiling proto files')
os_commands.proto_compile(
    base_ref=os_commands.create_path(paths.models, 'research'),
    proto_path=os_commands.create_path('..', paths.protoc, 'bin', 'protoc'),
    proto_files=os_commands.create_path('object_detection', 'protos', '*.proto')
)

print('Installing pip packages')
os_commands.pip_install('tensorflow==2.6.0')
os_commands.copy_file(
    src=os_commands.create_path(paths.models, 'research', 'object_detection', 'packages', 'tf2', 'setup.py'),
    dst=os_commands.create_path(paths.models, 'research')
)
os_commands.pip_install(os_commands.create_path(paths.models, 'research'))

# Verify
print('Verify if is ok')
test_path = os_commands.create_path(paths.models, 'research', 'object_detection', 'builders', 'model_builder_tf2_test.py')
os_commands.execute_script(test_path)