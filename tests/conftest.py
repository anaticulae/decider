# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import border.cli
import decider
import decider.cli
import fonts.cli
from tests.resources import RESOURCES


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
    result = utila.run(clean_and_run, cwd=root)
    assert result.returncode == utila.SUCCESS, result.stdout + result.stderr


if utila.LONGRUN:  # skip with --test=fast
    completed = utila.run('power --all', RESOURCES)  # pylint:disable=C0103
    assert completed.returncode == utila.SUCCESS, str(completed)

    install_and_run(
        decider.ROOT,
        decider.PACKAGE,
        [
            border.cli.PROCESS,
            decider.PROCESS,
            fonts.cli.PROCESS,
        ],
    )

pytest_plugins = 'pytester'  # pylint: disable=invalid-name
