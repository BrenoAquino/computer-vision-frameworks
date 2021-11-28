import os_commands

project_root = os_commands.create_path('..')

protoc = os_commands.create_path(project_root, 'protoc')

models = os_commands.create_path(project_root, 'models')

workspace = os_commands.create_path(project_root, 'workspace')
pre_trained_models = os_commands.create_path(workspace, 'pre_trained_models')
custom_models = os_commands.create_path(workspace, 'model')
dataset = os_commands.create_path(workspace, 'dataset')