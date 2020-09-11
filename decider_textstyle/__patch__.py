# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import protocol
import protocol.linter
import utila


def from_modules(
        modules: utila.Strings,
        tests: set = None,
        skips: set = None,
) -> protocol.Linter:
    status = []
    checkers = []
    solutions = []
    for name in modules:
        with contextlib.suppress(AttributeError):
            # support module type, ensure that module name is str
            name = name.__name__
        module = protocol.utils.module_fromname(name)
        solutions.extend(
            protocol.solution.parse_solutions(
                module,
                tests=tests,
                skips=skips,
            ))
        status.extend(protocol.linter.parse_active(module))
        checkers.extend(
            protocol.parse_checkers(
                module,
                tests=tests,
                skips=skips,
            ))
    result = protocol.from_solution(solutions, status, checkers=checkers)
    return result


protocol.from_modules = from_modules
