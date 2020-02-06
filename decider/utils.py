# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Store experimental code here"""

import collections
import importlib
import re
import typing

import protocol
import utila

Validators = typing.List[callable]


# TODO: MOVE TO PROTOCOL PACKAGE
def from_module(name: str) -> protocol.Linter:
    module = module_fromname(name)
    solution = parse_solutions(module)
    status = active(module)
    result = protocol.from_solution(solution, status)
    return result


def module_fromname(name: str):
    module = importlib.import_module(name)
    return module


SOLUTION = r'^SOLUTION_(?P<type>[A-Z]{0,1})(?P<number>\d{2,5})$'


def parse_solutions(module) -> protocol.Solutions:
    if isinstance(module, str):
        module = module_fromname(module)
    result = []
    for name, value in vars(module).items():
        matched = re.match(SOLUTION, name)
        if not matched:
            continue
        typ, number = matched['type'], int(matched['number'])  # pylint:disable=W0612
        try:
            title, message = value.split('\n\n', maxsplit=1)
        except ValueError:
            utila.error(f'{name} requires newline between headline and content')
            raise
        item = protocol.Text(title=title, msgid=number, description=message)
        result.append(item)
    return result


VALIDATOR = r'^check_(?P<number>\d{2,5})_'


def msgid(name) -> int:
    matched = re.match(VALIDATOR, name)
    if not matched:
        return None
    result = int(matched['number'])
    return result


def parse_checkers(module) -> Validators:
    if isinstance(module, str):
        module = module_fromname(module)
    result = []
    for name, value in vars(module).items():
        parsed = msgid(name)
        if not parsed:
            continue
        parsed = int(parsed)
        value.msgid = parsed
        if not hasattr(value, 'confidence'):
            # enable on default
            value.confidence = 1.0
        result.append(value)
    return result


def active(module):
    checkers = parse_checkers(module)
    result = [
        protocol.MessageStatus(
            msgid=msgid(item.__name__),
            active=item.confidence > 0.0,
            confidence=item.confidence,
        ) for item in checkers
    ]
    return result


def data_driver(**kwargs):
    # TODO: THERE MUST BE A BETTER WAY. PYTHONIC WAY.
    Driver = collections.namedtuple('Driver', kwargs.keys())
    driver = Driver(**kwargs)
    return driver


def confidence(value=1.0):

    def decorating_function(user_function):
        user_function.confidence = value
        return user_function

    return decorating_function
