import yaml


def parse_yaml(file):
    """
    :param file:
    :return:
    """
    with open(file, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)
