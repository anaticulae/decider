# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
from utila.test import install_and_run

from decider import ROOT


def test_installandrun(capsys):
    """Install groupme and run groupme --help to ensure basic function"""
    install_and_run(
        ROOT,
        'decider',
        'decider_border',
    )

    install_and_run(
        ROOT,
        'decider',
        'decider_fonts',
    )
