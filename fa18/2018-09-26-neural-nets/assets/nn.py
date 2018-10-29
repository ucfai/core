import plotly.offline as py
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go

import numpy as np

import itertools
import colorlover as cl

import os
os.chdir("..")
from __admin__.lib.algos.nn import NeuralNetwork

class Layer():
    start = 0
    max_n = 0
    n_hid = 0

    def __init__(self, size, name):
        if "hidden" in name:
            Layer.n_hid += 1
            self.name = "hidden" + str(Layer.n_hid)
        else:
            self.name = name
        self.n = size
        if (self.n > Layer.max_n):
            Layer.max_n = self.n

        self.at = Layer.start
        Layer.start += 1
        self.data = []

    def setup(self):
        self.x = self.__gen_x()
        self.y = self.__gen_y()
        self.data = go.Scatter(dict(
            name=self.name,
            mode="markers",
            marker=dict(
                size=40,
                line=dict(width=2),
                color=Network.colors[self.at % Network.n_layr],
            ),
            x=self.x,
            y=self.y,
        ))
        return self.data

    def __gen_x(self):
        return np.array([self.at for _ in np.arange(0, self.n, 1)])

    def __gen_y(self):
        at = (Layer.max_n - self.n) / 2
        return np.array([y for y in np.arange(at, self.n + at, 1)])

class Network():
    layers_size = [4, [6, 5, 7], 4]
    n_layr = 2 + len(layers_size[1])
    colors = cl.scales[str(n_layr)]["qual"]["Dark2"]

    def __init__(self):
        self.layers = [Layer(Network.layers_size[0], "input")]
        for x, hid in enumerate(Network.layers_size[1]):
            self.layers.append(Layer(hid, "hidden{}".format(x + 1)))
        self.layers.append(Layer(Network.layers_size[-1], "output"))

        self.pairs = [(x, x + 1) for x in range(Network.n_layr - 1)]

        self.weights = {}

    def build(self):
        self.scatter_layers = [layer.setup() for layer in self.layers]

    def connect(self):
        self.scatter_lines  = []
        for (x1, x2) in self.pairs:
            x, y = self.__connect(self.layers[x1], self.layers[x2])
            self.weights[str(x1)] = self.__paint_lines(x, y, Network.colors[x1 % Network.n_layr])
            self.scatter_lines += self.weights[str(x1)]
        pass

    def __connect(self, L1, L2):
        x = np.array([ np.array([
                [L1.x[n1], L2.x[n2], None] for n2 in range(L2.n)
            ]).flatten() for n1 in range(L1.n) ])
        y = np.array([ np.array([
                [L1.y[n1], L2.y[n2], None] for n2 in range(L2.n)
            ]).flatten() for n1 in range(L1.n) ])
        return x, y

    def __paint_lines(self, x, y, color):
        return [
            go.Scatter(
                x = x[_], y = y[_],
                line       = dict(color=color),
                showlegend = False,
            ) for _ in range(len(x))
        ]

    def combine(self):
        return self.scatter_lines + self.scatter_layers


def network():
    # nn = Network()
    # nn.build()
    # nn.connect()

    sliders_dict = dict(
        active = 0,
        yanchor = "top", xanchor = "left",
        currentvalue = dict(
            font = dict(size=20), prefix = "Year:",
            visible = True, xanchor = "right",
        ),
        transition = dict(duration = 300, easing = "cubic-in-out", ),
        pad = dict(b = 10, t = 50, ),
        len = 0.9, x = 0.1, y = 0, steps = [],
    )

    fig = {}
    # fig["data"  ] = nn.combine()
    fig["layout"] = {}
    fig["frames"] = []

    axes_tmpl = dict(
        ticks = '',
        showgrid = False,
        zeroline = False,
        autotick = True,
        showticklabels = False,
    )

    stages = [
        "start",
        "in_h1-vec", "in_h1-sig",
        "h1_h2-vec", "h1_h2-sig",
        "h2_ot-vec", "h2_ot-sft",
    ]

    fig["layout"]["title"] = "Stepping through a Neural Network"
    fig["layout"]["xaxis"] = axes_tmpl; fig["layout"]["yaxis"] = axes_tmpl
    fig["layout"]["hovermode"] = False
    fig["layout"]["showlegend"] = False
    # fig["layout"]["sliders"] = {
    #     'args': [
    #         'transition', {
    #             'duration': 400,
    #             'easing': 'cubic-in-out'
    #         }
    #     ],
    #     'initialValue': stages[0],
    #     'plotlycommand': 'animate',
    #     'values': stages,
    #     'visible': True
    # }

    # fig["layout"]["updatemenus"] = [
    #     {
    #         "buttons": [
    #             "args": [None, {"frame": {"duration": 500, "redraw": False},
    #                      "fromcurrent": True, "transition": {"duration": 300, "easing": "quadratic-in-out"}}],
    #             "label": "Step",
    #             "method": "animate",
    #         ]
    #     }
    # ]

    # print(nn.weights)

    # network_frames = []
    # for stage in stages:
    #     frame = {"data": [], "name": stage}

    nn_args = dict(
        nodes = np.array([4, 6, 5, 7, 4]),
        inp = np.array([
                [110, 255],
                [ 58, 255]
              ]),
        out = np.array([0.05, 0.9, 0.05, 0.0]),
        graphing = True,
        LR = 0.5,
    )
    nn = NeuralNetwork(nn_args)

    fig["data"] = nn.graph()

    return fig
