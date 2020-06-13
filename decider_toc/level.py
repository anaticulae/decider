# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import dataclasses

import configo
import iamraw

import decider_toc.utils


class TooFewChildren(decider_toc.utils.InvalidTocItems):  # pylint:disable=too-many-ancestors
    pass


class LevelToDeep(decider_toc.utils.InvalidTocItems):  # pylint:disable=too-many-ancestors
    pass


MAX_TOC_DEEPNESS = configo.HV_INT_PLUS(default=3).value


@dataclasses.dataclass
class TocValidationResult:
    level_to_deep: LevelToDeep = None
    too_few_children: TooFewChildren = None


def validate(toc: iamraw.Toc) -> TocValidationResult:
    too_few_children = validate_children(toc)
    deepness = validate_deepness(toc)

    result = TocValidationResult(
        level_to_deep=deepness,
        too_few_children=too_few_children,
    )
    return result


def validate_children(toc: iamraw.Toc) -> TooFewChildren:
    result = TooFewChildren()

    def godown(item: iamraw.toc.TocLinkMixin):
        if len(item.children) == 1:
            # If subpoint has only one children, it is not a subpoint.
            result.append(item)
            return
        for children in item:
            godown(children)

    for item in toc:
        godown(item)
    return result


def validate_deepness(toc: iamraw.Toc, maxdeep: int = None) -> LevelToDeep:
    if maxdeep is None:
        maxdeep = MAX_TOC_DEEPNESS

    result = LevelToDeep()

    def godown(item: iamraw.toc.TocLinkMixin):
        if item.level > maxdeep:
            result.append(item)
        for children in item:
            godown(children)

    for item in toc:
        godown(item)
    return result
