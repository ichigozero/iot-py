import operator
from functools import reduce


def get_dict_val(dict_obj, map_list):
    try:
        return reduce(operator.getitem, map_list, dict_obj)
    except (KeyError, TypeError):
        return ''
