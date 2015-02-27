from unittest import TestCase
from box import Box
from pdp_packing import get_non_blocking_boxes, get_block_boxes, stable_non_blocking_container_selector
from rpacker import RPacker


__author__ = 'Alex Baranov'


class TestPdpPacking(TestCase):
    """
    Contains tests for the pdp packing functions.
    """

    def test_non_blocking_selector(self):
        """
        Verify pdp container selection
        """
        packing_sequence = [
            Box(size=(1, 1, 1), name="a"),
            Box(size=(1, 1, 1), name="b"),
            Box(size=(1, 1, 1), name="c"),
            Box(name="a", kind="unpack"),
            Box(name="c", kind="unpack"),
            Box(name="b", kind="unpack"),
        ]

        packer = RPacker()
        container = Box(size=(30, 10, 10), bottom_left=(0, 0, 0))
        result, params = packer.pack(packing_sequence, (container, ),
                                     container_select_func=stable_non_blocking_container_selector)
        self.assertEqual(len(result), 0)
        self.assertEqual(len(params), 4)

        # check position. Most important is position of 'c'
        bboxes = filter(lambda x: x[1].name == 'c' and x[1].kind == 'solid' and x[0] == 'pack', params['actions'])
        self.assertEqual(len(bboxes), 1)
        self.assertEqual(bboxes[0][1].polus, (0, 0, 2))

        # check max x calculation
        self.assertEqual(params['max_x'], [1, 1, 1, 1, 1, 0])

    def test_non_block_box_search(self):
        """
        Verify the search algorithm for boxes that should not be blocked during packing.
        """

        packing_sequence = [
            Box(size=(1, 1), name="a"),
            Box(size=(1, 1), name="b"),
            Box(size=(1, 1), name="c"),
            Box(size=(1, 1), name="a", kind="unpack"),
            Box(size=(1, 1), name="c", kind="unpack"),
            Box(size=(1, 1), name="b", kind="unpack"),
        ]
        # check a
        a = packing_sequence[0]
        packed_elements = packing_sequence[:0]

        non_block_boxes = get_non_blocking_boxes(a, packing_sequence, packed_elements)
        self.assertIsNotNone(non_block_boxes)
        self.assertEqual(len(non_block_boxes), 0)

        # check non blocking for b
        b = packing_sequence[1]
        packed_elements = packing_sequence[:1]

        non_block_boxes = get_non_blocking_boxes(b, packing_sequence, packed_elements)
        self.assertIsNotNone(non_block_boxes)
        self.assertEqual(len(non_block_boxes), 1)
        self.assertEqual(non_block_boxes[0], packing_sequence[0])

        # check c box
        c = packing_sequence[2]
        packed_elements = packing_sequence[:2]
        non_block_boxes = get_non_blocking_boxes(c, packing_sequence, packed_elements)
        self.assertIsNotNone(non_block_boxes)
        self.assertEqual(len(non_block_boxes), 1)
        self.assertEqual(non_block_boxes[0], packing_sequence[0])

    def test_get_block_boxes_search(self):
        """
        Verify the search algorithm for boxes that should not block box to pack during packing.
        """
        packing_sequence = [
            Box(size=(2, 3, 4), name="d"),
            Box(size=(6, 7, 8), name="c"),
            Box(size=(1, 2, 3), name="a"),
            Box(size=(1, 2, 3), name="b"),
            Box(name="a", kind="unpack"),
            Box(name="b", kind="unpack"),
            Box(name="c", kind="unpack"),
            Box(name="d", kind="unpack"),
        ]

        # check d
        d = packing_sequence[0]
        packed_elements = packing_sequence[:0]

        non_block_boxes = get_block_boxes(d, packing_sequence, packed_elements)
        self.assertIsNotNone(non_block_boxes)
        self.assertEqual(len(non_block_boxes), 0)

        # check c
        c = packing_sequence[1]
        packed_elements = (d,)
        non_block_boxes = get_block_boxes(c, packing_sequence, packed_elements)
        self.assertIsNotNone(non_block_boxes)
        self.assertEqual(len(non_block_boxes), 1)
        self.assertEqual(non_block_boxes[0], d)

        # check a
        a = packing_sequence[2]
        c.polus = (2, 0, 0)
        packed_elements = (d, c)
        non_block_boxes = get_block_boxes(a, packing_sequence, packed_elements)
        self.assertIsNotNone(non_block_boxes)
        self.assertEqual(len(non_block_boxes), 2)
        self.assertEqual(non_block_boxes[0], d)
        self.assertEqual(non_block_boxes[1], c)

    def test_pdp_packing(self):
        """
        Verify the pap packing sample scenario.
        """
        packing_sequence = [
            Box(size=(2, 3, 4), name="d"),
            Box(size=(6, 7, 8), name="c"),
            Box(size=(1, 2, 3), name="a"),
            Box(size=(1, 2, 3), name="b"),
            Box(name="a", kind="unpack"),
            Box(name="b", kind="unpack"),
            Box(name="c", kind="unpack"),
            Box(name="d", kind="unpack"),
        ]

        container = Box(size=(10, 7, 10), bottom_left=(0, 0, 0))
        packer = RPacker()
        result, params = packer.pack(packing_sequence, (container, ),
                                     container_select_func=stable_non_blocking_container_selector)
        self.assertEqual(len(result), 0)
        self.assertEqual(len(params['actions']), 8)
        self.assertEqual(params['actions'][0][1].polus, (0, 0, 0))
        self.assertEqual(params['actions'][1][1].polus, (2, 0, 0))
        self.assertEqual(params['actions'][2][1].polus, (8, 0, 0))
        self.assertEqual(params['actions'][3][1].polus, (8, 0, 3))
        self.assertEqual(params['actions'][4][0], "unpack")
        self.assertEqual(params['actions'][4][1].name, "a")
        self.assertEqual(params['actions'][5][0], "unpack")
        self.assertEqual(params['actions'][5][1].name, "b")
        self.assertEqual(params['actions'][6][0], "unpack")
        self.assertEqual(params['actions'][6][1].name, "c")
        self.assertEqual(params['actions'][7][0], "unpack")
        self.assertEqual(params['actions'][7][1].name, "d")

        self.assertEqual(params['max_x'], [2, 8, 9, 9, 9, 8, 2, 0])