from unittest import TestCase
from rpacker import RPacker
from box import Box

__author__ = 'Alex Baranov'


class TestRPacker(TestCase):
    """
    Test for RPacker
    """

    def setUp(self):
        """
        The setup test method.
        """
        self.packer = RPacker()

    def test_included_box_remove(self):
        """
        Verify the included containers are correctly removed
        """
        containers = [Box(size=(2, 1)),
                      Box(size=(1, 3), bottom_left=(1, 0)),
                      Box(size=(1, 2), bottom_left=(1, 1)),
                      Box(size=(1, 1), bottom_left=(3, 3))]

        not_included_containers = self.packer.remove_included_containers(containers)
        self.assertEqual(len(not_included_containers), 3)
        self.assertIn(containers[0], not_included_containers)
        self.assertIn(containers[1], not_included_containers)
        self.assertIn(containers[3], not_included_containers)
        self.assertNotIn(containers[2], not_included_containers)

    def test_split_included_containers(self):
        """
        Verify the included containers remove function.
        """
        containers = [Box(size=(4, 3)),
                      Box(size=(2, 5))]

        element = Box(size=(1, 1), bottom_left=(1, 4))

        split_containers = self.packer.split_intersected_containers(containers, element)
        self.assertEqual(len(split_containers), 3)

        self.assertEqual(split_containers[0].size, (4, 3))
        self.assertEqual(split_containers[0].polus, (0, 0))

        self.assertEqual(split_containers[1].size, (1, 5))
        self.assertEqual(split_containers[1].polus, (0, 0))

        self.assertEqual(split_containers[2].size, (2, 4))
        self.assertEqual(split_containers[2].polus, (0, 0))

    def test_pack_sample_scenarios(self):
        """
        Verify the packing sample scenarios.
        """
        c = Box(size=(2, 2), bottom_left=(1, 1))
        p = Box(size=(1, 1))

        packed, params = self.packer.pack(boxes=(p, ), containers=(c, ))
        self.assertEqual(len(packed), 1)

        p1 = packed.pop()
        self.assertIsNotNone(p1)
        self.assertEqual(p1.size, (1, 1))
        self.assertEqual(p1.polus, (1, 1))

    def test_pack_sample_scenario2(self):
        """
        Verify the packing sample scenarios #2.
        """

        c = Box(size=(5, 8), bottom_left=(0, 0))
        elements = [Box(size=(4, 2)),
                    Box(size=(3, 3)),
                    Box(size=(2, 4))]

        packed, params = self.packer.pack(elements, containers=(c, ))
        self.assertEqual(len(packed), 3)

        p1, p2, p3 = packed

        # check first packed
        self.assertIsNotNone(p1)
        self.assertEqual(p1.size, (4, 2))
        self.assertEqual(p1.polus, (0, 0))

        # check second packed.
        self.assertIsNotNone(p2)
        self.assertEqual(p2.size, (3, 3))
        self.assertEqual(p2.polus, (0, 2))

        # check third packed.
        self.assertIsNotNone(p3)
        self.assertEqual(p3.size, (2, 4))
        self.assertEqual(p3.polus, (3, 2))