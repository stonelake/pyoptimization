__author__ = "Alex Baranov"

from random import randrange
from visual import *

from reports import ReportsBuilder


class BoxDrawer(object):
    """
    Draws the boxes
    """

    def __init__(self, packing_params=None, display_labels=True, **kwargs):
        """
        Start the box drawing.
        """
        self.win = display(title='Packing results', background=(0.1, 0.1, 0.1), randrange=scene.autoscale)
        self.win.select()
        self.display_labels = display_labels

        # create frames
        self.arrows_frame = frame()
        self.containers_frame = frame()
        self.boxes_frame = frame()
        self.labels_frame = frame()

        # draw arrows
        self.__draw_arrows()

        # assign default variables
        self.container_color = kwargs.get("container_color", color.green)

        # packing params
        self.pack_params = packing_params

        self.actions = []
        self.action_index = 0
        if packing_params:
            self.actions = packing_params.get("actions", [])

    @classmethod
    def show_packing_results(cls, result, params, containers):
        """
        Displays the packing results.
        """
        bd = BoxDrawer(packing_params=params)
        bd.add_containers(containers)
        bd.add_boxes(result)
        bd.display()

    def __get_random_color(self):
        """
        Generates the random color.
        """
        return [randrange(0, 255) / 255. for _ in range(3)]

    def add_boxes(self, boxes, change_action_pointer=True):
        """
        Draws all the boxes that should or were packed.
        """
        for pbox in boxes:
            bcolor = self.__get_random_color()
            box(frame=self.boxes_frame, pos=pbox.center, size=pbox.size, color=bcolor)
            label(frame=self.labels_frame, pos=pbox.center, box=0,
                  text='name={}\npolus={}\nsize={}'.format(pbox.name, pbox.polus, pbox.size))

        # if some boxes were added set the actions index to max
        if boxes and change_action_pointer:
            self.action_index = len(self.actions)

    def remove_box(self, box):
        """
        Removes bo from the display.
        """
        for element in filter(lambda x: x.pos == box.center and x.size == box.size, self.boxes_frame.objects):
            element.visible = False

            # remove also label
            for label in filter(lambda x: x.pos == box.center, self.labels_frame.objects):
                label.visible = False

    def add_containers(self, containers, random_color=False, opacity=None, centered_labels=False):
        """
        Add container to the screen.
        """

        op = opacity or 0.1

        for index, container in enumerate(containers):
            if random_color:
                c = self.__get_random_color()
            else:
                c = self.container_color

            box(frame=self.containers_frame, pos=container.center, size=container.size, opacity=op, color=c)

            if centered_labels:
                pos = container.polus
            else:
                pos = container.diagonal_polus
            label(frame=self.labels_frame, pos=pos, box=0,
                  text='Container #{}\npolus={}\nsize={}'.format(index, container.polus, container.size))

    def __draw_arrows(self):
        """
        Draws the x,y,z arrows.
        """
        #x
        arrow(frame=self.arrows_frame, pos=(0, 0, 0), axis=(10, 0, 0), shaftwidth=0.01)
        label(frame=self.arrows_frame, pos=(10, 0, 0), box=0, text='X')

        #y
        arrow(frame=self.arrows_frame, pos=(0, 0, 0), axis=(0, 10, 0), shaftwidth=0.01)
        label(frame=self.arrows_frame, pos=(0, 10, 0), box=0, text='Y')

        #z
        arrow(frame=self.arrows_frame, pos=(0, 0, 0), axis=(0, 0, 10), shaftwidth=0.01)
        label(frame=self.arrows_frame, pos=(0, 0, 10), box=0, text='Z')

        for obj in self.arrows_frame.objects:
            obj.color = color.orange

    def __draw_action(self, action_pair):
        name = action_pair[0]
        b = action_pair[1]

        if name == "pack":
            self.add_boxes((b, ), change_action_pointer=False)
        elif name == "unpack":
            self.remove_box(b)

    def __remove_all_boxes(self):
        for element in self.boxes_frame.objects:
            element.visible = False
            # remove labels
            for label in filter(lambda x: x.pos == element.pos,
                                self.labels_frame.objects):
                label.visible = False

    def display(self):
        print "-------------------------------------------------------"
        while 1:
            rate(100)
            if self.win.kb.keys:
                s = self.win.kb.getkey()
                if len(s) == 1:
                    if s == 'l' or s == 'L':
                        if self.display_labels:
                            self.labels_frame.visible = False
                            self.display_labels = False
                        else:
                            self.labels_frame.visible = True
                            self.display_labels = True

                    # display actions
                    if s == 'n' or s == 'N':
                        if not self.actions:
                            continue
                        else:
                            if len(self.actions) == self.action_index:
                                self.action_index = 0
                                if self.boxes_frame.objects:
                                    # remove non-unpacked boxes
                                    self.__remove_all_boxes()

                                print "Packing completed \n\n"
                            else:
                                if self.actions[self.action_index][0] == "pack":
                                    frmt = "Packing"
                                else:
                                    frmt = "Unpacking"

                                print "{} box: '{}'".format(frmt, self.actions[self.action_index][1])
                                self.__draw_action(self.actions[self.action_index])
                                self.action_index += 1

                    # display reports
                    if s == 'r' or s == 'R':
                        if self.pack_params:
                            ReportsBuilder.show_dynamic_report(self.pack_params)

