from  urllib.request import urlretrieve
from _picker import pick

import _paths as paths

import zipfile
import os_commands

os_options = [
    'Linux - aarch - 64',
    'Linux - ppcle - 64',
    'Linux - s390 - 64',
    'Linux - x86 - 32',
    'Linux - x86 - 64',
    'macOS - x86 - 64',
    'Windows - 32',
    'Windows - 64',
    'Custom URL'
]

os_urls = [
    'https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-linux-aarch_64.zip',
    'https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-linux-ppcle_64.zip',
    'https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-linux-s390_64.zip',
    'https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-linux-x86_32.zip',
    'https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-linux-x86_64.zip',
    'https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-osx-x86_64.zip',
    'https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-win32.zip',
    'https://github.com/protocolbuffers/protobuf/releases/download/v3.19.1/protoc-3.19.1-win64.zip'
]

# Create protoc folder
os_commands.create_dir(paths.protoc)

# Get URL to download repo/branch/version
title_1 = 'To configure protoc you need to tell me the correct path for your O.S.'
title_2 = 'You can see all releases in https://github.com/protocolbuffers/protobuf/releases'
title_3 = 'If you choose the O.S. i will use v3.19.1. You can choose manual URL to input the URL with any S.O. and version.'
title_input = 'Please choose your O.S.: '
title = title_1 + '\n' + title_2 + '\n' + title_3 + '\n' + title_input
option, index = pick(os_options, title, indicator='=>', default_index=0)

if option == 'Custom URL':
    url = input('Enter the url: ') 
else:
    url = os_urls[index]

print('Downloading protoc')
protoc_project_path = os_commands.create_path(paths.protoc, 'protoc.zip')
urlretrieve(url, protoc_project_path)

print('Extracting package')
with zipfile.ZipFile(protoc_project_path, 'r') as zip_ref:
    zip_ref.extractall(paths.protoc)
os_commands.delete_file(protoc_project_path)

print('Setup protoc')
protoc_exec_path = os_commands.create_path(paths.protoc, 'bin', 'protoc')
os_commands.give_permission(protoc_exec_path)