# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Store experimental code here"""
import importlib
import re

import protocol
import utila


# TODO: MOVE TO PROTOCOL PACKAGE
def from_module(name: str) -> protocol.Linter:
    module = importlib.import_module(name)
    try:
        solution = module.SOLUTION
    except AttributeError:
        raise ValueError(f'could not create solver, no SOLUTION: {name}')
    try:
        status = module.STATUS
    except AttributeError:
        utila.debug(f'no `STATUS` provided in {name}')
        status = []
    result = protocol.from_solution(solution, status)
    return result


SOLUTION = r'^SOLUTION_(?P<type>[A-Z]{0,1})(?P<number>\d{2,5})$'


def parse_solutions(module) -> protocol.Solutions:
    result = []
    for name, value in vars(module).items():
        matched = re.match(SOLUTION, name)
        if not matched:
            continue
        typ, number = matched['type'], int(matched['number'])  # pylint:disable=W0612
        title, message = value.split('\n\n', maxsplit=1)
        item = protocol.Text(title=title, msgid=number, description=message)
        result.append(item)
    return result
