from unittest import TestCase
from box import Box

__author__ = 'Alex Baranov'


class TestBox(TestCase):
    """
    Set of test for the Box class
    """

    def test_create(self):
        """
        Verify that Box can be created
        """
        rect = Box((1, 2, 3))
        self.assertIsNotNone(rect)
        self.assertEqual(rect.size, (1, 2, 3))

        # check the default bottom left property was set
        self.assertEqual(rect.polus, (0, 0, 0))

        # check non-default polus position
        rect2 = Box((1, 2, 3), [-1, 2, 0])
        self.assertEqual(rect2.polus, [-1, 2, 0])

    def test_create_invalid(self):
        """
        Verify invalid scenarios of the rect creation.
        """
        self.assertRaises(ValueError, Box, (1, 2, 3), (4, 5))
        self.assertRaises(ValueError, Box, (1, 2), (1, 4, 5))
        self.assertRaises(ValueError, Box, (1, 2), (1, ))

    def test_diagonal_polus_calculation(self):
        """
        Tests the calculation of the opposite to polus corner
        """
        rect = Box((1, 2, 3))
        self.assertEqual(rect.diagonal_polus, [1, 2, 3])

        # change polus position
        rect.polus = (3, 0, 2)
        self.assertEqual(rect.diagonal_polus, [4, 2, 5])

        # change size position
        rect.size = (3, 2, 1)
        self.assertEqual(rect.diagonal_polus, [6, 2, 3])

    def test_center_calculation(self):
        """
        Verify calculation of the center position.
        """

        rect = Box((2, 3, 4))
        self.assertEqual(rect.center, [1, 1.5, 2])

        # change polus
        rect.polus = (2, 10, -3)
        self.assertEqual(rect.center, [3, 11.5, -1])

        # change size
        rect.size = (4, 2, 4)
        self.assertEqual(rect.center, [4, 11, -1])

    def test_area_calculation(self):
        """
        Verify  calculation of the box calculation.
        """
        p = Box(size=(2, 3, 4))
        self.assertEqual(p.get_area(), 24)

        # change size
        p.size = (4, 3, 1, 4)
        self.assertEqual(p.get_area(), 48)

    def test_point_including_check_valid(self):
        """
            Verify check whether the point is within the box.
            """
        p = Box(size=(2, 3, 4))
        valid_test_points = [(1, 1, 1), (0, 0, 0), (2, 3, 4), (1, 2, 3)]
        for pnt in valid_test_points:
            self.assertTrue(p.includes_point(pnt))

        # change position
        p.polus = 5, 1, 3
        self.assertTrue(p.includes_point((7, 4, 6)))

    def test_point_including_check_invalid(self):
        """
        Verify check whether the point is within the box.
        """
        p = Box(size=(2, 3, 4), bottom_left=(1, 2, 3))
        invalid_test_points = [(1, 1, 1), (0, 0, 0), (0, 3, 4), (1, 12, 3)]
        for pnt in invalid_test_points:
            self.assertFalse(p.includes_point(pnt), "Checking point '{0}'".format(pnt))

    def test_touch_valid(self):
        """
        Verify touch check works correctly.
        """
        p = Box(size=(2, 3, 4), bottom_left=(1, 2, 3))
        touched_boxes = (Box(size=(1, 2, 3)),
                         Box(size=(1, 2, 3), bottom_left=(3, 5, 7)),
                         Box(size=(1, 2, 3), bottom_left=(1, 5, 3)),
                         Box(size=(1, 2, 3), bottom_left=(1, 2, 7)),
                         Box(size=(1, 10, 30), bottom_left=(0, 1, 1)),)

        for par in touched_boxes:
            self.assertTrue(p.touches(par))

    def test_touch_invalid(self):
        """
        Verify touch invalid scenarios.
        """
        p = Box(size=(2, 2, 2), bottom_left=(3, 2, 4))
        touched_boxes = (Box(size=(1, 2, 3)),
                         Box(size=(1, 2, 3), bottom_left=(1, 1, 1)),
                         Box(size=(2, 2, 2), bottom_left=(6, 5, 3)))

        for par in touched_boxes:
            self.assertFalse(p.touches(par))

    def test_intersect_valid(self):
        """
        Verify intersect valid scenarios.
        """
        p = Box(size=(2, 2, 2), bottom_left=(1, 1, 1))
        valid_boxes = (Box(size=(2, 3, 3)),
                       Box(size=(6, 2, 3)))

        for par in valid_boxes:
            self.assertTrue(p.intersects(par), "Checking p: {}".format(par))

    def test_intersect_invalid(self):
        """
        Verify intersect invalid scenarios.
        """
        p = Box(size=(2, 3, 4), bottom_left=(1, 2, 3))
        invalid_boxes = (Box(size=(1, 2, 3)),
                         Box(size=(0.5, 0, 0)),
                         Box(size=(1, 2, 3), bottom_left=(3, 5, 7)),
                         Box(size=(1, 2, 3), bottom_left=(1, 5, 3)),)

        for par in invalid_boxes:
            self.assertFalse(p.intersects(par), "Checking p: {}".format(par))

    def test_can_accept(self):
        """
        Check the can_accept method,
        """
        test_list = (Box(size=(4, 4, 4), bottom_left=(0, 0, 0)),
                     Box(size=(4, 2, 2), bottom_left=(-10, -10, -10)),)

        test_list2 = (Box(size=(2, 2, 2), bottom_left=(10, 10, 10)),
                      Box(size=(1, 2, 2), bottom_left=(1, 2, 2)),)

        for p1, p2 in zip(test_list, test_list2):
            self.assertTrue(p1.can_accept(p2), "Checking : {}, {}".format(p1, p2))

    def test_includes_valid(self):
        """
        Verify the box include check.

        """
        p = Box(size=(2, 2, 2), bottom_left=(1, 1, 1))
        valid_boxes = (Box(size=(2, 2, 2), bottom_left=(1, 1, 1)),
                       Box(size=(1, 1, 1), bottom_left=(1, 1, 1)),
                       Box(size=(1, 1, 1), bottom_left=(2, 2, 2)))
        for par in valid_boxes:
            self.assertTrue(p.includes(par), "Checking p: {}".format(par))

        # check 2d
        b1 = Box(size=(1, 3), bottom_left=(1, 0))
        b2 = Box(size=(1, 1), bottom_left=(1, 2))

        self.assertTrue(b1.includes(b2), "Checking p: {}".format(b1))

    def test_includes_invalid(self):
        """
        Verify the box include check (invalid scenarios).

        """
        p = Box(size=(2, 2, 2), bottom_left=(1, 1, 1))
        invalid_boxes = (Box(size=(2, 2.1, 2), bottom_left=(1, 1, 1)),
                         Box(size=(1, 1, 1), bottom_left=(0, 0, 1)),
                         Box(size=(1, 1, 1), bottom_left=(3, 3, 3)))
        for par in invalid_boxes:
            self.assertFalse(p.includes(par), "Checking p: {}".format(par))

    def test_free_box_list(self):
        """
        Verify calculation of the free containers.
        """
        p1 = Box(size=(4, 3))
        p2 = Box(size=(2, 1))
        free_containers = p1.find_free_containers(p2)
        self.assertEqual(len(free_containers), 2, "Check that only 2 containers were generated")

        # check first container
        self.assertEqual(free_containers[0].size, (2, 3))
        self.assertEqual(free_containers[0].polus, (2, 0))

        # check second container
        self.assertEqual(free_containers[1].size, (4, 2))
        self.assertEqual(free_containers[1].polus, (0, 1))

    def test_free_box_list2(self):
        """
        Verify calculation of the free containers additional scenarios.
        """
        c = Box(size=(2, 5), bottom_left=(0, 0))
        p = Box(size=(1, 1), bottom_left=(1, 4))

        free_containers = c.find_free_containers(p)

        self.assertEqual(len(free_containers), 2, "Check that only 2 containers were generated")

        # check first container
        self.assertEqual(free_containers[0].size, (1, 5))
        self.assertEqual(free_containers[0].polus, (0, 0))

        # check second container
        self.assertEqual(free_containers[1].size, (2, 4))
        self.assertEqual(free_containers[1].polus, (0, 0))

    def test_free_box_list3(self):
        """
        Verify calculation of the free containers additional scenarios 3d.
        """
        c = Box(size=(4, 5, 10), bottom_left=(0, 2, 0))
        b = Box(size=(3, 3, 3), bottom_left=(0, 0, 2))

        free_containers = c.find_free_containers(b)
        self.assertEqual(len(free_containers), 4)

        #1
        self.assertEqual(free_containers[0].size, (1, 5, 10))
        self.assertEqual(free_containers[0].polus, (3, 2, 0))

        #2
        self.assertEqual(free_containers[1].size, (4, 4, 10))
        self.assertEqual(free_containers[1].polus, (0, 3, 0))

        #3
        self.assertEqual(free_containers[2].size, (4, 5, 5))
        self.assertEqual(free_containers[2].polus, (0, 2, 5))

        #4
        self.assertEqual(free_containers[3].size, (4, 5, 2))
        self.assertEqual(free_containers[3].polus, (0, 2, 0))

        print free_containers

    def test_is_blocked_valid_2d(self):
        """
        Verify is_blocked for 2d cases.
        """
        c1 = Box(size=(2, 2), bottom_left=(0, 0))

        check_boxes = [Box(size=(1, 1), bottom_left=(3, 1)),
                       Box(size=(1, 1), bottom_left=(3, 1.5)),
                       Box(size=(1, 1), bottom_left=(3, 0)),
                       Box(size=(1, 1), bottom_left=(2, -0.5))]

        for box in check_boxes:
            check_result = c1.is_blocked(box)
            self.assertTrue(check_result)

        # check false scenarios
        check_boxes = [Box(size=(1, 1), bottom_left=(3, 2)),
                       Box(size=(1, 1), bottom_left=(3, -1)),
                       Box(size=(1, 1), bottom_left=(3, 3)),
                       Box(size=(1, 1), bottom_left=(0, 2)),
                       Box(size=(1, 1), bottom_left=(1, 2)),
                       Box(size=(1, 1), bottom_left=(2, 2))]

        for box in check_boxes:
            check_result = c1.is_blocked(box)
            self.assertFalse(check_result)

    def test_is_blocked_valid_3d(self):
        """
        Verify is_blocked for 3d cases.
        """
        c1 = Box(size=(2, 2, 2), bottom_left=(0, 0, 0))
        check_boxes = [Box(size=(1, 3, 1), bottom_left=(2, 0, 1))]

        for box in check_boxes:
            check_result = c1.is_blocked(box)
            self.assertTrue(check_result)

    def test_is_blocked_valid_2d_axes(self):
        """
        Verify is_blocked for 2d cases.
        """
        c1 = Box(size=(2, 2), bottom_left=(0, 0))

        check_boxes = [Box(size=(1, 1), bottom_left=(3, 1)),
                       Box(size=(1, 1), bottom_left=(3, 1.5)),
                       Box(size=(1, 1), bottom_left=(3, 0)),
                       Box(size=(1, 1), bottom_left=(0, 2)),
                       Box(size=(1, 1), bottom_left=(1, 3)),
                       Box(size=(1, 1), bottom_left=(2, -0.5))]

        for box in check_boxes:
            check_result = c1.is_blocked(box, axes=(1, 1))
            self.assertTrue(check_result)

        # check false scenarios
        check_boxes = [Box(size=(1, 1), bottom_left=(2, 2)),
                       Box(size=(1, 1), bottom_left=(2, 3)),
                       Box(size=(1, 1), bottom_left=(3, 3)),
                       Box(size=(1, 1), bottom_left=(3, 2))]

        for box in check_boxes:
            check_result = c1.is_blocked(box)
            self.assertFalse(check_result)

    def test_is_basis_valid_2d(self):
            """
            Verify basis check for 2d cases.
            """
            c1 = Box(size=(2, 2), bottom_left=(0, 0))

            check_boxes = [Box(size=(1, 1), bottom_left=(1, 2)),
                           Box(size=(2, 1), bottom_left=(0, 2)),
                           Box(size=(1, 1), bottom_left=(0, 2))]

            for box in check_boxes:
                check_result = c1.is_basis_for(box)
                self.assertTrue(check_result)

            # check false scenarios
            check_boxes = [Box(size=(1, 1), bottom_left=(0, 2.1)),
                           Box(size=(1, 1), bottom_left=(-0.1, 2)),
                           Box(size=(1, 1), bottom_left=(2.1, 2)),
                           Box(size=(2.2, 1), bottom_left=(0, 2)),
                           Box(size=(2, 2), bottom_left=(3, 0)),
                           Box(size=(2.2, 1), bottom_left=(-0.1, 2))]

            for box in check_boxes:
                check_result = c1.is_basis_for(box)
                self.assertFalse(check_result)

    def test_is_basis_valid_2d_axes(self):
        """
        Verify basis check for 2d cases.
        """
        c1 = Box(size=(2, 2), bottom_left=(0, 0))

        check_boxes = [Box(size=(1, 1), bottom_left=(2, 0)),
                       Box(size=(1, 2), bottom_left=(2, 0))]

        for box in check_boxes:
            check_result = c1.is_basis_for(box, axes=(1, 0))
            self.assertTrue(check_result)

        # check false scenarios
        check_boxes = [Box(size=(1, 1), bottom_left=(2.1, 0)),
                       Box(size=(1, 3), bottom_left=(2, 0)),
                       Box(size=(1, 1), bottom_left=(2, 1.1))]

        for box in check_boxes:
            check_result = c1.is_basis_for(box, axes=(1, 0))
            self.assertFalse(check_result)

    def test_equal(self):
        """
        Verify box comparing.
        """
        b1 = Box(size=(2, 2), bottom_left=(0, 0))
        b2 = Box(size=(2, 2), bottom_left=(0, 1))

        self.assertEqual(b1, b2)

        # invalid scenarios
        check_boxes = [Box(size=(2, 2.1), bottom_left=(0, 0)),
                       Box(size=(2, 3), bottom_left=(0, 0)),
                       Box(size=(1, 1), bottom_left=(0, 0)),
                       Box(size=(2, 2), bottom_left=(0, 0), name="test"),
                       Box(size=(2, 2), bottom_left=(0, 0), kind="test")]

        for check_box in check_boxes:
            self.assertNotEqual(b1, check_box)