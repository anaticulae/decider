# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from pytest import fixture
from utila import SUCCESS
from utila import run

from tests.resources import DOCU_TWINE


@fixture
def rawmaker(tmpdir):
    root = str(tmpdir)
    cmd = 'rawmaker -i %s -o %s' % (DOCU_TWINE, root)
    completed = run(cmd)
    assert completed.returncode == SUCCESS, str(completed)
    return root
