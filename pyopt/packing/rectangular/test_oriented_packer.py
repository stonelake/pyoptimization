from unittest import TestCase
from box import Box
from oriented_packing import oriented_container_selector, oriented_packer

__author__ = 'Alex Baranov'


class TestOrientedPacker(TestCase):
    """
    Contains the unit tests for the oriented packer.
    """

    def test_default_packer_valid(self):
        """
        Verify the default non-orthogonal packer
        """

        # test for 2d
        c = Box(size=(2, 3), bottom_left=(1, 1))
        p = Box(size=(1, 3))

        pack_result, r = oriented_packer(c, p)

        self.assertTrue(pack_result)
        self.assertEqual(r.polus, (1, 1))
        self.assertEqual(p.polus, (0, 0))
        self.assertEqual(p.size, (1, 3))
        self.assertEqual(c.polus, (1, 1))

        # test for 3d
        c = Box(size=(3, 3, 3), bottom_left=(1, 2, 0))
        p = Box(size=(2, 2, 2))
        pack_result, r = oriented_packer(c, p)

        self.assertTrue(pack_result)
        self.assertEqual(p.polus, (0, 0, 0))
        self.assertEqual(r.polus, (1, 2, 0))
        self.assertEqual(r.size, (2, 2, 2))
        self.assertEqual(c.polus, (1, 2, 0))
        self.assertEqual(c.size, (3, 3, 3))

    def test_default_packer_invalid(self):
        """
        Verify the default non-orthogonal packer invalid scenarios
        """

        # test for 2d
        c = Box(size=(2, 3), bottom_left=(1, 1))
        p = Box(size=(1, 3.1), bottom_left=(0, 0))

        pack_result, r = oriented_packer(c, p)

        self.assertFalse(pack_result)
        self.assertEqual(p.polus, (0, 0))
        self.assertEqual(p.size, (1, 3.1))
        self.assertEqual(c.polus, (1, 1))
        self.assertIsNone(r)

        # test for 3d
        c = Box(size=(3, 3, 3), bottom_left=(1, 2, 0))
        p = Box(size=(4, 1, 1))
        pack_result, r = oriented_packer(c, p)

        self.assertFalse(pack_result)
        self.assertIsNone(r)
        self.assertEqual(p.polus, (0, 0, 0))
        self.assertEqual(c.polus, (1, 2, 0))
        self.assertEqual(c.size, (3, 3, 3))

    def test_default_container_selector_valid(self):
        """
        Verify the default container selector valid scenarios
        """
        containers = [Box(size=(4, 2), bottom_left=(2, 0)),
                      Box(size=(2, 2), bottom_left=(0, 3))]

        p = Box(size=(2, 2))
        c, b = oriented_container_selector(containers, p)
        self.assertIsNotNone(c)
        self.assertEqual(c.polus, (0, 3))
        self.assertEqual(c.size, (2, 2))

        self.assertIsNotNone(b)
        self.assertEqual(b.polus, (0, 3))
        self.assertEqual(b.size, (2, 2))

    def test_default_container_selector_valid2(self):
        """
        Verify the default container selector valid scenarios 2
        """
        containers = [Box(size=(4, 2), bottom_left=(2, 0)),
                      Box(size=(2, 2), bottom_left=(0, 3))]

        p = Box(size=(3, 2))
        c, b = oriented_container_selector(containers, p)
        self.assertIsNotNone(c)
        self.assertEqual(c.polus, (2, 0))
        self.assertEqual(c.size, (4, 2))

        self.assertIsNotNone(b)
        self.assertEqual(b.polus, (2, 0))
        self.assertEqual(b.size, (3, 2))

    def test_default_container_selector_invalid(self):
        """
        Verify the default container selector invalid scenarios
        """
        containers = [Box(size=(4, 2), bottom_left=(2, 0)),
                      Box(size=(2, 2), bottom_left=(0, 3))]

        p = Box(size=(3, 3))
        c, b = oriented_container_selector(containers, p)
        self.assertIsNone(c)
        self.assertIsNone(b)

        containers = []
        c, b = oriented_container_selector(containers, p)
        self.assertIsNone(c)
        self.assertIsNone(c,b)
