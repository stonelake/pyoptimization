__author__ = 'Alex Baranov'

#from reports import ReportsBuilder
from pdp_packing import stable_non_blocking_container_selector
from orthogonal_packing import orthogonal_packer
#from drawer import BoxDrawer
from rpacker import RPacker
from box import Box
from optparse import OptionParser


# define the command line arguments
parser = OptionParser()
parser.add_option("-o", "--output", dest="output_filename",
                  help="write solution report to FILE", metavar="FILE", default='output.txt')
parser.add_option("-b", "--boxes", dest="boxes_filename",
                  help="the file to read boxes data from", metavar="FILE")
parser.add_option("-n", "--boxes_count", dest="boxes_count",
                  help="the file to read boxes data from", type='int')
parser.add_option("-r", "--route", dest="route",
                  help="the route data")
parser.add_option("-c", "--container", dest="container",
                  help="the route data")
parser.add_option("-p", "--partial-route", action="store_true", dest="is_partial_route",
                  help="specifies whether the route is partial")



def pack_boxes(boxes, container,
               container_select_func=stable_non_blocking_container_selector,
               packer=orthogonal_packer, # allows rotations
               allowed_rotation_axes=(1, 0, 1), # allows rotation only by X and Z axes
               is_partial_route=False,
               **kwargs):
    """
    Packs the defined sequence (as string) of nodes to visit.

    :param boxes: the list of boxes to pack
    :param container:  the container to pack boxes in.
    :param draw_results: specifies whether the we should draw results
    :param container_select_func: the container packing select function
    :param kwargs: other keyword arguments
    """
    pp = RPacker()
    result, params = pp.pack(boxes, (container, ),
                             container_select_func=container_select_func,
                             packer=packer,
                             allowed_rotation_axes=allowed_rotation_axes,
                             **kwargs)
    return is_packing_successful(result, params, boxes, container, is_partial_route), result, params
 

def read_korobki_file(box_number, korobki_file):
    """
    Returns the dictionary with the boxes. The keys are the box indexes.
    """
    res = {}
    with open(korobki_file, 'r') as kfile:
        for index, line in enumerate(kfile):
            if 0 < index <= box_number:
                splited = line.split(' ')[4:]
                l = float(splited[0].replace(',', '.'))
                w = float(splited[1].replace(',', '.'))
                h = float(splited[2].replace(',', '.'))
                weight = float(splited[3].lstrip('\n').replace(',', '.'))
                res[index] = Box(size=(l, w, h), weight=weight, name=index)

    return res


def parse_container_data(container_string):
    h, w, l, m = str.split(container_string)
    return Box(size=(float(h.replace(',', '.')), float(w.replace(',', '.')), float(l.replace(',', '.'))),
               weight=float(m.replace(',', '.')))


def pack_route(boxes_dict, route, cont, is_partial_route, **kwargs):
    """
    Packs the boxes to the containers according the defined route data.

    Returns:
        - tuple (pack result: bool, packed_boxes: list, packing result parameters: dict)

    """
    box_sequence = {}
    values = route.split()
    box_number = len(boxes_dict)
    box_sequence['price'] = values[-1]
    box_sequence['route'] = []
    for box_index in values[:-1]:
        box_index = int(box_index)
        if box_index <= box_number:
            # add the packing box
            box_sequence['route'].append(boxes_dict[box_index])
        else:
            # add unpack
            box_sequence['route'].append(Box(name=boxes_dict[box_index - box_number].name, kind="unpack"))

    return pack_boxes(box_sequence['route'], cont, is_partial_route=is_partial_route, **kwargs)


def pack_from_files(box_number,
                    korobki_file,
                    pdp_file,
                    container=Box(size=(20, 20, 20), weight=100),
                    container_select_func=stable_non_blocking_container_selector,
                    **kwargs):
    """
    Gets box data from the file.
    """
    # read and parse korobki file
    kfile = open(korobki_file, 'r')
    rfile = open(pdp_file, 'r')

    # parse boxes from kfile
    boxes = {}
    for index, line in enumerate(kfile):
        if 0 < index <= box_number:
            splited = line.split(' ')[4:]
            l = float(splited[0].replace(',', '.'))
            w = float(splited[1].replace(',', '.'))
            h = float(splited[2].replace(',', '.'))
            weight = float(splited[3].lstrip('\n').replace(',', '.'))
            boxes[index] = Box(size=(l, w, h), weight=weight, name=index)

    # read packing routes
    box_sequences = []
    for route in rfile:
        box_sequence = {}
        values = route.split()
        box_sequence['price'] = values[-1]
        box_sequence['route'] = []
        for box_index in values[:-1]:
            box_index = int(box_index)
            if box_index <= box_number:
                # add the packing box
                box_sequence['route'].append(boxes[box_index])
            else:
                # add unpack
                box_sequence['route'].append(Box(name=boxes[box_index - box_number].name, kind="unpack"))
        box_sequences.append(box_sequence)

    # pass all the box sequences one by one
    for bb in box_sequences:
        res, packed_boxes, params = pack_boxes(bb['route'], container, container_select_func=container_select_func,
                                               **kwargs)
        if res:
            return bb['price'], packed_boxes, params, container


def is_packing_successful(packing_results, packing_params, boxes_to_pack, container, is_partial_route):
    """
    Checks whether the packing was successful and all the boxes were delivered.
    """
    if not is_partial_route:
        return len(packing_results) == 0 and len(packing_params['actions']) == len(boxes_to_pack) and all(
            container.weight >= w for w in packing_params['weights'])
    else:
        return len(packing_params['actions']) == len(boxes_to_pack)

#def draw_results(result, params, container):
#    BoxDrawer.show_packing_results(result, params, (container,))
#
#
#def show_reports(params, container, **kwargs):
#    ReportsBuilder.show_dynamic_report(params, container, **kwargs)


if __name__ == "__main__":
    (options, args) = parser.parse_args()
    print options

    # read the korobki file first
    boxes = read_korobki_file(options.boxes_count, options.boxes_filename)
    container = parse_container_data(options.container)
    res = pack_route(boxes, options.route, container, 
                     place_axes=(1, 0, 2), 
                     is_partial_route=options.is_partial_route)
    print res[0]

    # saving to file
    with open(options.output_filename, 'w') as o:
        o.writelines(map(lambda s: repr(s) + '\n', res))

    #price, packed_boxes, params, container = pack_from_files(4,
    #                                                         'Korobki.txt',
    #                                                         'PDP.txt',
    #                                                         place_axes=(1, 0, 2))
    #print('Route price is ' + price)
    #show_reports(params, container, pdf=False)
    #draw_results(packed_boxes, params, container)
