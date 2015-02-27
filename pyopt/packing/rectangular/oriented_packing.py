from copy import deepcopy
from box import Box

__author__ = 'Alex Baranov'


def oriented_packer(container, rect, **kwargs):
    """
    Packs rect to the container without changing rect orthogonal orientation.

    Arguments:
        container : the box that should accept another box (acceptor).
        rect: the box to pack into container.

    Return:
     Pair (bool, rect):
        - bool: indicates whether the rect was packed to the container.
        - rect: the resulting packed box.

    """
    assert isinstance(container, Box)
    assert isinstance(rect, Box)

    if not container.can_accept(rect):
        return False, None

    # pack element to the bottom left corner of the container
    c = deepcopy(rect)
    c.polus = container.polus[:]
    return True, c


def oriented_container_selector(available_containers, box, packer=None, **kwargs):
    """
    Selects the best container for the box.
    """
    packer = packer or oriented_packer

    valid_containers = []
    for c in available_containers:
        result, result_box = packer(c, box)
        if result:
            valid_containers.append((c, result_box))

    # return none if we can't find valid containers
    if not valid_containers:
        return None, None

    # sort containers by polus X coordinate
    return sorted(valid_containers, key=lambda cont: cont[0].polus[0])[0]