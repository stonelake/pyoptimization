from pyopt.packing.rectangular.drawer import BoxDrawer

__author__ = "Alex Baranov"

from rpacker import RPacker
from unittest import TestCase
from box import Box
from pdp_packing import non_blocking_container_selector, stable_non_blocking_container_selector


class TestDrawer(TestCase):
    """
    Check the drawer options
    """
    def setUp(self):
        """
        Setups test
        """
        self.packer = RPacker()

    def test_packing1(self):
        """
        Verify packing scenario 1.
        """
        c = Box(size=(30, 10, 10), bottom_left=(0, 0, 0))
        elements = [Box(size=(4, 2, 2)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(3, 3, 3)),
                    Box(size=(2, 4, 2))
                    ]
        result, params = self.packer.pack(elements, (c,), container_select_func=stable_non_blocking_container_selector,
                                          place_axes=(0, ))
        BoxDrawer.show_packing_results(result, params, (c,))
