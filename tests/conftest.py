# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

from utila import SUCCESS
from utila import install_and_run
from utila import run
from utila.test import LONGRUN

from border.cli import PROCESS_NAME as BORDER_PROCESS_NAME
from decider import PACKAGE
from decider import ROOT
from fonts.cli import PROCESS_NAME as FONTS_PROCESS_NAME
from tests import TEST_DATA


# TODO: MOVE TO UTILA->TEST
def install_and_run(root, package, executable=None):
    """Install and run --help to ensure basic function"""
    executable = executable if executable else package
    if isinstance(executable, str):
        executable = executable.split()
    uninstall = 'pip uninstall %s -y' % package

    executable = ' && '.join(['%s --help' % item for item in executable])
    install = 'python setup.py install && %s ' % executable

    clean_and_run = uninstall + ' && ' + install
    completed = run(clean_and_run, cwd=root)
    assert completed.returncode == SUCCESS, completed.stdout + completed.stderr


if LONGRUN:  # skip with --test=fast
    completed = run('power --all', TEST_DATA)  # pylint:disable=C0103
    assert completed.returncode == SUCCESS, str(completed)

    install_and_run(
        ROOT,
        PACKAGE,
        [
            BORDER_PROCESS_NAME,
            FONTS_PROCESS_NAME,
        ],
    )
pytest_plugins = 'pytester'  # pylint: disable=invalid-name
