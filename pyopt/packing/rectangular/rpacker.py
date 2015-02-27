__author__ = "Alex Baranov"

from oriented_packing import oriented_packer, oriented_container_selector
from copy import deepcopy
from box import Box


class RPacker(object):
    """
    Class is used to rectangular elements to the rectangular containers.
    """

    def __init__(self, **kwargs):
        """
        Creates instance of the RPacker class.

        Arguments:
            - rn: number of dimensions
            - allow_rotation: allows rotation of the elements.

        """
        super(RPacker, self).__init__()

        # by default rotation is allowed.
        self.allow_rotation = kwargs.get("allow_rotation", True)

    def pack(self, boxes,
             containers,
             packer=None,
             container_select_func=None,
             split_included_containers=False,
             verbose=True, **kwargs):
        """
        Packs rectangles to the containers.

        Arguments:
            - boxes: the list of the rectangles.
            - containers: the list of containers.
            Should be provided in the same form as 'rectangles'.
            - packer: function that packs one box to one container. Should accept two parameters:
                (container, rect)
            - container_select_func: function that select the containers for the box. Accepts three
             parameters: (all_available_containers, box to pack, packer function). Should return the
             container or None (when unable to find valid container for box)

        Returns:
            - the list of packed rectangles.
        """

        # TODO Add description or all optional parameters

        packer = packer or oriented_packer
        container_select_func = container_select_func or oriented_container_selector
        result = []
        if verbose:
            print "Packing boxes '{0}' to containers '{1}'".format(map(str, boxes), map(str, containers))
        internal_containers = deepcopy(list(containers))
        internal_elements = deepcopy(list(boxes))
        actions = []
        max_x = []
        loading_coefs = []
        weights = []

        for i, rectangle in enumerate(internal_elements):

            if rectangle.kind == "unpack":
                # remove already packed box if present
                for packed in filter(lambda x: x.name == rectangle.name and x.kind == "solid", result):

                    if verbose:
                        print "Unpacking box: {}".format(packed)
                    result.remove(packed)

                    # add container instead of removed control
                    parent_container = filter(lambda c: c.includes(packed), containers)
                    if parent_container:
                        cc = Box(bottom_left=packed.polus,
                                 size=tuple(
                                     parent_container[0].size[i] - packed.polus[i] for i in range(len(packed.polus))))
                        internal_containers.append(cc)
                        if split_included_containers:
                            internal_containers = self.remove_included_containers(internal_containers)

                        # remove intersected containers
                        for packed_element in result:
                            internal_containers = self.split_intersected_containers(internal_containers, packed_element)

                    # add actions
                    actions.append(("unpack", packed))

                    # recalculate max_x and loading
                    max_x.append(self.__calculate_max_x(result))
                    loading_coefs.append(self.__calculate_loading(result, containers))
                    weights.append(self.__calculate_weights(result))
            else:
                # select the best container
                target_container, packed_element = container_select_func(internal_containers, rectangle,
                                                                         packer=packer,
                                                                         packed_boxes=result,
                                                                         all_boxes=boxes,
                                                                         **kwargs)

                # if target container is null, return the currently packed elements.
                if not target_container:
                    break

                if verbose:
                    print "Packing box: {} ".format(packed_element)
                result.append(packed_element)

                actions.append(("pack", packed_element))

                # calculate solution dynamic parameters
                max_x.append(self.__calculate_max_x(result))
                loading_coefs.append(self.__calculate_loading(result, containers))
                weights.append(self.__calculate_weights(result))

                # get new containers
                new_containers = target_container.find_free_containers(packed_element)

                # remove target container
                internal_containers.remove(target_container)

                # add new containers
                internal_containers += new_containers

                # remove included containers
                if split_included_containers:
                    internal_containers = self.remove_included_containers(internal_containers)

                # remove intersected containers
                internal_containers = self.split_intersected_containers(internal_containers, packed_element)

        params = {"actions": actions, "max_x": max_x, "loading": loading_coefs, "weights": weights}
        return result, params

    def fit_by_rotation(self, rect, container):
        """
        Rotates the rectangle to fit it into container.
        The polus of the rectangle won't be affected.

        Arguments:
            - rect: rectangle to fit.
            - container: container to fit rectangle into.
            - minimize_index: the minimize direction. Specifies the index of the dimension to minimize
        """

        res = sorted(rect.size)
        if all((container.size[index] - res[index]) >= 0 for index in xrange(len(res))):
            return rect

    def remove_included_containers(self, containers):
        """
        Removes containers that's are completely within another container.

        Arguments:
            - containers: the list of all available containers.
        """

        not_included = [cont for index, cont in enumerate(containers)
                        if all([not cc.includes(cont) for num, cc in enumerate(containers)
                                if num != index])]
        return not_included

    def split_intersected_containers(self, containers, box):
        """
        Splits the containers that are intersected by the packed box.

        Arguments:
            - containers:: the list of all available containers.
            - box: packed box.

        Returns:
            - a new resulting list of containers.
        """
        result = []
        for container in containers:
            if box.intersects(container):
                result += container.find_free_containers(box)
            else:
                result.append(container)

        return result

    def __calculate_max_x(self, packed_boxes):

        if packed_boxes:
            b = max(packed_boxes, key=lambda box: box.polus[0] + box.size[0])
            return b.polus[0] + b.size[0]
        else:
            return 0

    def __calculate_loading(self, packed_boxes, initial_containers):
        if packed_boxes:
            b = sum(map(lambda p: p.get_area(), packed_boxes)) / float(
                sum(map(lambda p: p.get_area(), initial_containers)))
            return b
        else:
            return 0

    def __calculate_weights(self, packed_boxes):
        if packed_boxes:
            return sum(b.weight for b in packed_boxes)
        else:
            return 0