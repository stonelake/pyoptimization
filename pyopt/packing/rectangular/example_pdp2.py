from box import Box
from pdp_packing import stable_non_blocking_container_selector
from orthogonal_packing import orthogonal_packer
from drawer import BoxDrawer
from reports import ReportsBuilder
from rpacker import RPacker

if __name__ == "__main__":
    packing_sequence = [
        Box(size=(8, 50, 32), name="a", weight=32),
        Box(size=(33, 29, 8), name="b", weight=5),
        Box(size=(20, 44, 26), name="c", weight=2),
        Box(size=(15, 16, 30), name="d", weight=1),
        Box(name="a", kind="unpack"),
        Box(name="b", kind="unpack"),
        Box(name="c", kind="unpack"),
        Box(name="d", kind="unpack")

    ]

    packer = RPacker()
    container = Box(size=(100, 100, 100), bottom_left=(0, 0, 0), weight=25)
    result, params = packer.pack(packing_sequence, (container, ),
                                 packer=orthogonal_packer,
                                 container_select_func=stable_non_blocking_container_selector,
                                 place_axes=(0, 2, 1),  # the container selection criteria. Getting the lowest container,
                                 axes_priorities=(1, 2, 0),  # the rotation priorities.
                                 # First try to rotate to minimize by Y axis
                                 allowed_rotation_axes=(1, 0, 1))  # allow rotation only by X and Z axes

    BoxDrawer.show_packing_results(result, params, (container,))
    #ReportsBuilder.show_dynamic_report(params, container=container, pdf=False)
