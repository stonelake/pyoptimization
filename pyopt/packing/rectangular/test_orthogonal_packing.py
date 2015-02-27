__author__ = 'Alex Baranov'

from unittest import TestCase
from box import Box
from orthogonal_packing import orthogonal_packer

__author__ = 'Alex Baranov'


class TestOrthogonalPacker(TestCase):
    """
    Contains the unit tests for the orthogonal packer.
    """
    def test_orthogonal_packed_valid(self):
        """
        Verify the valid orthogonal packing scenarios
        """
        c = Box(size=(5, 5, 5))
        b = Box(size=(2, 3, 1))

        r = orthogonal_packer(c, b, allowed_rotation_axes=(1, 0, 1))

        # check packing result
        self.assertTrue(r[0])

        # check packed box parameters
        self.assertEqual(r[1].size, (1,3,2))