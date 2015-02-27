__author__ = 'Alex Baranov'

from oriented_packing import oriented_packer
from operator import itemgetter
from itertools import ifilter


def get_non_blocking_boxes(current_box, all_boxes, packed_boxes):
    """
    Get boxes that are not allowed to block with the current box.
    """

    result = []
    current_box_index = all_boxes.index(current_box) if current_box in all_boxes else None

    f = filter(lambda x: x.name == current_box.name and x.kind == "unpack", all_boxes)
    current_unpack = f[0] if f else None

    if not current_box_index or not current_unpack:
        return result

    current_unpack_index = all_boxes.index(current_unpack)

    # get the packed boxes in all boxes collection
    for packed_box in packed_boxes:
        current_packed = next(ifilter(lambda x: x.name == packed_box.name and x.kind == packed_box.kind, all_boxes), None)
        packed_index = all_boxes.index(current_packed)
        #packed_index = all_boxes.index(packed_box) if packed_box in all_boxes else -1

        if packed_index != -1 and packed_index < current_box_index:
            # check if current box is within the delivery interval of the packed box
            f = filter(lambda x: x.name == packed_box.name and x.kind == "unpack", all_boxes)

            unpack_index = -1
            if f:
                unpack_index = all_boxes.index(f[0])

            # first check: current box should not block another box that will be unpacked after current
            if unpack_index != -1 and packed_index < current_box_index < unpack_index < current_unpack_index:
                # packed box should not be bocked by current box
                result.append(packed_box)

    return result


def get_block_boxes(current_box, all_boxes, packed_boxes):
    """
    Get boxes that are not allowed to block with the current box.
    """
    result = []
    current_box_index = all_boxes.index(current_box) if current_box in all_boxes else None
    current_unpack = next(ifilter(lambda x: x.name == current_box.name and x.kind == "unpack", all_boxes), None)

    if not current_box_index or not current_unpack:
        return result

    current_unpack_index = all_boxes.index(current_unpack)

    for packed_box in packed_boxes:
        # find index of the packed box
        current_packed = next(ifilter(lambda x: x.name == packed_box.name and x.kind == packed_box.kind, all_boxes), None)
        packed_index = all_boxes.index(current_packed)

        if packed_index != -1 and packed_index < current_box_index:
            # check if already packed box blocks the current box
            f = filter(lambda x: x.name == packed_box.name and x.kind == "unpack", all_boxes)

            unpack_index = -1
            if f:
                unpack_index = all_boxes.index(f[0])

            if unpack_index != -1 and packed_index < current_box_index < current_unpack_index < unpack_index:
                result.append(packed_box)

    return result


def non_blocking_container_selector(available_containers,
                                    box,
                                    packer=None,
                                    packed_boxes=None,
                                    all_boxes=None, **kwargs):
    """
    Selects the best container for so the target do not block already packed containers.
    """
    packer = packer or oriented_packer
    axes = kwargs.get("axes", __get_default_axes(box))

    valid_containers = []

    # get  the list of boxes that should not be blocked by current box.
    non_blocking_boxes = get_non_blocking_boxes(box, all_boxes, packed_boxes)

    # get the list of boxes that should not block the current box
    blocking_boxes = get_block_boxes(box, all_boxes, packed_boxes)

    for c in available_containers:
        b, rect = packer(c, box, **kwargs)

        # also need to perform second block check:
        # current box should not be blocked by the packed boxes
        # if current unpack will took place prior unpacking the packed box.
        # Example: d c -a- b a b c d. Current box is a. 'a' should not be blocked by 'c' and 'd'
        check2 = all(not rect.is_blocked(bb, axes=axes) for bb in blocking_boxes)

        if b and __does_not_block_all(rect, non_blocking_boxes, axes) and check2:
            valid_containers.append((c, rect))

    # return none if we can't find valid containers
    if not valid_containers:
        return None, None

    # sort containers by polus X coordinate
    return sorted(valid_containers, key=lambda cont: cont[0].polus[0])[0]


def stable_non_blocking_container_selector(available_containers,
                                           box,
                                           packer=None,
                                           packed_boxes=None,
                                           all_boxes=None, **kwargs):
    """
    Selects the best container for the box.
    """
    packer = packer or oriented_packer

    # get the non block directions.
    # by default unpack boxes in +X direction and do not block box that is below another
    # so default value for axes is (1,1,0)
    axes = kwargs.get("axes", __get_default_axes(box))

    # the place axes defines the sorting order for the the available containers.
    # for example (1,2,0) defines that containers will be sorted b Y then b Z and then by X
    if len(box.polus) > 2:
        place_axes = kwargs.get("place_axes", (0, 1, 2))
    else:
        place_axes = kwargs.get("place_axes", (0, 1))

    non_blocking_boxes = get_non_blocking_boxes(box, all_boxes, packed_boxes)

    # get the list of boxes that should not block the current box
    blocking_boxes = get_block_boxes(box, all_boxes, packed_boxes)

    valid_containers = []
    for c in available_containers:
        pack_result, rect = packer(c, box, **kwargs)

        if pack_result:
            if packed_boxes:

                check2 = all(not rect.is_blocked(bb, axes=axes) for bb in blocking_boxes)
                floor = min(available_containers, key=lambda x: x.polus[1]).polus[1]
                if any([rect.polus[1] == floor or pb.is_basis_for(rect) for pb in packed_boxes]) and \
                        __does_not_block_all(rect, non_blocking_boxes, axes) and check2:
                    valid_containers.append((c, rect))
            else:
                valid_containers.append((c, rect))

    # return none if we can't find valid containers
    if not valid_containers:
        return None, None

    return sorted(valid_containers, key=lambda cont: itemgetter(*place_axes)(cont[0].polus))[0]


def __does_not_block_all(packed_box, non_blocking_boxes, axes):
    return all(not pp.is_blocked(packed_box, axes=axes) for pp in non_blocking_boxes)


def __get_default_axes(box):
    default_axes = [0] * len(box.size)
    default_axes[:2] = [1, 1]
    return default_axes
