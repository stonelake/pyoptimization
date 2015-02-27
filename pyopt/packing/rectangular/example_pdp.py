from box import Box
from pdp_packing import stable_non_blocking_container_selector
from orthogonal_packing import orthogonal_packer
from drawer import BoxDrawer
from reports import ReportsBuilder
from rpacker import RPacker

if __name__ == "__main__":
    packing_sequence = [
        Box(size=(1, 1, 1), name="a", weight=10),
        Box(size=(2, 2, 2), name="b", weight=5),
        Box(size=(2, 3, 1), name="c", weight=2),
        Box(size=(1, 1, 3), name="d", weight=1),
        Box(name="c", kind="unpack"),
        Box(size=(1, 1, 2), name="e", weight=5),
        Box(size=(1, 1, 1), name="f", weight=10),
        Box(name="a", kind="unpack"),
        Box(name="f", kind="unpack"),
        Box(name="e", kind="unpack"),
        Box(size=(2, 2, 2), name="g", weight=7),
        Box(name="d", kind="unpack"),
        Box(size=(1, 1, 1), name="k", weight=8),
        Box(name="b", kind="unpack"),
        Box(name="k", kind="unpack"),
        Box(name="g", kind="unpack"),
    ]

    packer = RPacker()
    container = Box(size=(4, 5, 5), bottom_left=(0, 0, 0), weight=25)
    result, params = packer.pack(packing_sequence, (container, ),
                                 packer=orthogonal_packer,
                                 container_select_func=stable_non_blocking_container_selector,
                                 place_axes=(2, 1, 0),  # the container selection criteria. Getting the lowest container,
                                 axes_priorities=(0, 1, 2),  # the rotation priorities.
                                 # First try to rotate to minimize by Y axis
                                 allowed_rotation_axes=(1, 0, 1))  # allow rotation only by X and Z axes

    BoxDrawer.show_packing_results(result, params, (container,))
    #ReportsBuilder.show_dynamic_report(params, container=container, pdf=False)
