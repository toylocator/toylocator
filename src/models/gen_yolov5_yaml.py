import os
import yaml

data_dir = '/data/'

def gen_data_yaml(inventory_path, yaml_dir):
    """
    A function that updates the nc and names config in data.yaml and
    the nc config in custom_yolov5.yaml based on label inventory.
    Parameters:
        - inventory_path: file path to label_inventory.txt
        - yaml_path: file path to data.yaml and custom_yolov5.yaml
    """
    data_yaml_path = os.path.join(yaml_dir, 'data.yaml')
    # model_yaml_path = yaml_path + 'custom_yolov5.yaml'

    # Read number of classes from label inventory list
    with open(inventory_path, 'r') as file:
        class_set = list(file.read().splitlines())

    # # Load existing data.yaml
    # with open(data_yaml_path) as f:
    #     data = yaml.load(f, Loader=yaml.FullLoader)

    data_yaml = {}
    # Update configurations
    data_yaml['nc'] = len(class_set)
    data_yaml['names'] = class_set
    data_yaml['train'] = "/data/train/images"
    data_yaml['val'] = "/data/validate/images"
    # data_yaml['test'] = "/data/test/images"

    # Update data.yaml
    with open(data_yaml_path, 'w') as f:
        yaml.dump(data_yaml, f, default_flow_style=None)

    # Load existing custom_yolov5.yaml
    # with open(model_yaml_path) as f:
    #     data = yaml.load(f, Loader=yaml.FullLoader)

    # Update cthonfigurations
    data_yaml['nc'] = len(class_set)

    # Update data.yaml
    # yaml.dump does not support nested lists
    # with open(model_yaml_path, 'w') as f:
    #    f.write(yaml.dump(data, default_flow_style=None))


if __name__ == '__main__':

    gen_data_yaml(os.path.join(data_dir, 'label_inventory.txt'), data_dir)
