import os
import subprocess
import sys

__author__ = 'oleksii.baranov'

import matplotlib.pyplot as plt


class ReportsBuilder(object):
    """
    Responsible to build all the packing reports.
    """

    def __init__(self):
        super(ReportsBuilder, self).__init__()

    @classmethod
    def show_dynamic_report(cls, packing_results, container=None, pdf=True):
        """
        Shows the dynamic reports
        """

        plt.title("Dynamic reports")
        dynamic_values_x = packing_results['max_x']
        dynamic_values_loading = packing_results['loading']
        actions = packing_results['actions']

        # add loading by X dynamic data
        cls.__add_subplot(311, dynamic_values_x, "X loading", '-ro', actions)

        # add loading coef data
        cls.__add_subplot(312, dynamic_values_loading, "Loading coefficient", '-bo', actions)

        # show weights
        cls.__add_subplot(313, packing_results['weights'], "Weight dynamic", '-go', actions)
        if container:
            cls.__add_subplot(313, [container.weight for _ in packing_results['weights']],
                              "Max allowed weight",
                              '-r', actions)

        if pdf:
            file = "dynamic_report.pdf"
            plt.savefig(file)
            if sys.platform == 'linux2':
                subprocess.call(["xdg-open", file])
            else:
                os.startfile(file)
        else:
            plt.show()

    @classmethod
    def __add_subplot(cls, position, data, label, line_format, actions, show_grid=True):
        """
        Add the subplot to a graph.
        """
        ax = plt.subplot(position)

        plt.plot(data, line_format, label=label)
        plt.grid(show_grid)
        plt.xticks(range(len(data)), ["{}{}".format("" if act[0] == "pack" else "-", act[1].name) for act in actions])
        maxval = 1
        if max(data) > 1:
            maxval = 10
        plt.axis([0, len(data), 0, max(data) + maxval])

        handles, labels = ax.get_legend_handles_labels()
        leg = ax.legend(handles, labels, fancybox=True)
        leg.get_frame().set_alpha(0.3)