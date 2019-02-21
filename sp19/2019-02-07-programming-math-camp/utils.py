__all__ = ["graph_x", "graph_x2", "graph_chain", "graph_saddle"]

from typing import Tuple

import numpy as np
import plotly.offline as py
import plotly.graph_objs as go

def graph_x(val: int = 20):
    x = np.linspace(-0.5 * val, 1.5 * val, num=200)
    y = np.power(x, 1)
    
    data = [go.Scatter(x=x, y=y)]
    
    layout = go.Layout(
        title="Graph of f(x) = x",
        autosize=True,
        margin=dict(l=65, r=50,
                    b=65, t=90,)
    )
    
    return py.iplot(go.Figure(data=data, layout=layout))

def graph_x2(val: int = 10):
    x = np.linspace(-1. * val, 1. * val, num=200)
    y = np.power(x, 2) - x + 4
    
    data = [go.Scatter(x=x, y=y)]
    
    layout = go.Layout(
        title="Graph of f(x) = x^2 - x + 4",
        autosize=True,
        margin=dict(l=65, r=50,
                    b=65, t=90,)
    )
    
    return py.iplot(go.Figure(data=data, layout=layout))

def graph_chain(val: int = 10):
    x = np.linspace(-1. * val, 1. * val, num=200)
    y = np.power(3 * np.power(x, 2) + x - 4, 3)
    
    data = [go.Scatter(x=x, y=y)]
    
    layout = go.Layout(
        title="Graph of f(x) = (3x^2 + x - 4)^3",
        autosize=True,
        margin=dict(l=65, r=50,
                    b=65, t=90,)
    )
    
    return py.iplot(go.Figure(data=data, layout=layout))

def graph_saddle(val: int = 10):
    x = np.linspace(-1. * val, 1. * val, num=200)
    y = np.linspace(-1. * val, 1. * val, num=200)
    y_grid, x_grid = np.meshgrid(x, y)
    z = (y_grid * np.power(x_grid, 2)) - 3 * np.power(y_grid, 2)
    
    data = [go.Surface(x=x, y=y, z=z)]
    
    layout = go.Layout(
        title="Graph of f(x, y) = yx^2 - 3y^2",
        autosize=True,
        margin=dict(l=65, r=50,
                    b=65, t=90,)
    )
    
    return py.iplot(go.Figure(data=data, layout=layout))