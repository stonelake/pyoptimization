__author__ = 'Alex Baranov'

from box import Box
from itertools import permutations
from operator import itemgetter
from copy import deepcopy


def orthogonal_packer(container, rect, axes_priorities=None, allowed_rotation_axes=None, **kwargs):
    """
    Packs rect to the container. Rotation of packed are allowed on 90.

    Arguments:
        container : the box that should accept another box (acceptor).
        rect: the box to pack into container.

    Return:
     Pair (bool, rect):
        - bool: indicates whether the rect was packed to the container.
        - rect: the resulting packed box.
    """

    # by default rotate to fit first by X then by Y then by Z
    axes_priorities = axes_priorities or tuple(a for a in range(len(container.size)))

    # by default allow rotation by any axe
    allowed_rotation_axes = allowed_rotation_axes or tuple(1 for _ in range(len(container.size)))
    assert isinstance(container, Box)
    assert isinstance(rect, Box)

    allowed_sizes = __get_all_allowed_box_permutations(rect, axes_priorities, allowed_rotation_axes)
    copied_box = deepcopy(rect)

    for s in allowed_sizes:
        copied_box.size = s
        if container.can_accept(copied_box):
            copied_box.polus = container.polus[:]
            return True, copied_box

    return False, None


def __get_all_allowed_box_permutations(rect, axes, allowed_rotation_axes):
    """
    Gets the list of allowed box size permutations.
    """
    # get valid(allowed) permutations
    valid_permutations = []
    for p in permutations(rect.size):
        restricted_indexes = (i for i, r in enumerate(allowed_rotation_axes) if r == 0)
        if all(rect.size[ind] == p[ind] for ind in restricted_indexes):
            valid_permutations.append(p)

    # sort list by defined axes order
    return sorted(valid_permutations, key=itemgetter(*axes))

if __name__ == "__main__":
    pass
