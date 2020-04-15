# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Test reference
==============

Test references in linter solutions message that they exists in
`writers` docs.
"""

import glob
import os

import protocol
import utila
import writers

import decider


def test_all_references_exists():
    """Parse all files to extract invalid references out of templates."""
    error = False
    collected = collect_message()
    for path, template in collected:
        invalid = writers.validate_template(template)
        error |= bool(invalid)
        if invalid:
            utila.error(path)
            utila.error(invalid)
    assert not error


def pyfiles():
    result = []
    projects = ['border', 'decider']
    for item in projects:
        source = os.path.join(decider.ROOT, item)
        with utila.chdir(source):
            collected = glob.glob('**/*.py', recursive=True)
            collected = [os.path.join(item, it) for it in collected]
            result.extend(collected)
    return result


def collect_message():
    result = []
    for pyfile in pyfiles():
        path = pyfile.replace('.py', '')
        path = utila.forward_slash(path)
        path = path.replace('/', '.')
        if '__' in path:
            # no messages in __init__ and __main__ packages
            continue
        parsed = protocol.parse_solutions(path)
        if not parsed:
            continue
        for item in parsed:
            result.append((path, item.description))
    return result
