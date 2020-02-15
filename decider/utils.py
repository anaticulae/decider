# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Store experimental code here :)"""

import collections
import dataclasses
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


@dataclasses.dataclass(unsafe_hash=True)
class BoundingLocation:
    """The location defines the object on which the Finding belongs to.
    Defines rectangle which can be highlighted in further presentation
    steps. The rectangle is the simplest highlighting method.

    .. code-block :: none

        Examples for location:

        bounding    b(137.0;145.0;123.0;232.0)p5
    """
    # TODO: MOVE TO PROTOCOL
    page: int = -1
    shortcut: str = None
    value: tuple = None

    PATTERN = r'(?P<shortcut>b)\((?P<tuple>((\d+\.\d+;{0,1}){4}))\)p(?P<page>\d+)'

    def __str__(self) -> str:
        joined = ';'.join([str(item) for item in self.value])  # pylint:disable=E1133
        raw = f'b({joined})p{self.page}'
        return raw

    @classmethod
    def fromstr(cls, raw: str):
        assert raw, 'require input'
        matched = re.match(BoundingLocation.PATTERN, raw)
        if not matched:
            return None

        page, shortcut, value = int(matched['page']), 'b', None
        value = matched['tuple'].split(';')
        value = utila.roundme(*[float(item) for item in value])
        value = tuple(value)
        shortcut = matched['shortcut']
        result = cls(page=page, shortcut=shortcut, value=value)
        return result

    @classmethod
    def fromtuple(cls, bounding: tuple, page: int):
        return cls(shortcut='b', page=page, value=bounding)
