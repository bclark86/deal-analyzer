import os
from deal_analyzer.utils import parse_yaml


def generate_deal_specs():
    return parse_yaml('config.yml')
