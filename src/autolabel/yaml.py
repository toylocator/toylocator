import os
import yaml

PATH = '/data/'
inventory_path = PATH + '/data/label_inventory.txt'

def yaml_update(inventory_path, yaml_path):
    """
    A function that updates the nc and names config in data.yaml and
    the nc config in custom_yolov5.yaml based on label inventory.
    Parameters:
        - inventory_path: file path to label_inventory.txt
        - yaml_path: file path to data.yaml and custom_yolov5.yaml
    """

    data_yaml_path = yaml_path + 'data.yaml'
    # model_yaml_path = yaml_path + 'custom_yolov5.yaml'

    # Read number of classes from label inventory list
    with open(inventory_path, 'r') as file:
        class_set = list(file.read().splitlines())

    # Load existing data.yaml
    with open(data_yaml_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    # Update configurations
    data['nc'] = len(class_set)
    data['names'] = class_set

    # Update data.yaml
    with open(data_yaml_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=None)

    # Load existing custom_yolov5.yaml
    # with open(model_yaml_path) as f:
    #     data = yaml.load(f, Loader=yaml.FullLoader)

    # Update cthonfigurations
    data['nc'] = len(class_set)

    # Update data.yaml
    ### yaml.dump does not support nested lists
    #with open(model_yaml_path, 'w') as f:
    #    f.write(yaml.dump(data, default_flow_style=None))

yaml_update(inventory_path, PATH)
