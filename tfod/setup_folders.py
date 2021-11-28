import _paths as path

import os_commands

# Create default folder for CV project with TensorFlow Object Detection API
os_commands.create_dir(path.workspace)
os_commands.create_dir(path.pre_trained_models)
os_commands.create_dir(path.custom_models)
os_commands.create_dir(path.dataset)