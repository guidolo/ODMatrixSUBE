from matplotlib import pyplot
from shapely.geometry import LineString
from shapely.geometry import Point
#from figures import SIZE

COLOR = {
    True:  '#6699cc',
    False: '#ffcc33'
    }

def v_color(ob):
    return COLOR[ob.is_simple]

def plot_coords(ax, ob):
    x, y = ob.xy
    ax.plot(x, y, 'o', color='#999999', zorder=1)

def plot_bounds(ax, ob):
    x, y = zip(*list((p.x, p.y) for p in ob.boundary))
    ax.plot(x, y, 'o', color='#000000', zorder=1)

def plot_line(ax, ob):
    x, y = ob.xy
    ax.plot(x, y, color=v_color(ob), alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)

def nuevoGraf():
    #fig = pyplot.figure(1, figsize=SIZE, dpi=90)
    fig = pyplot.figure(1,  dpi=180)
    return fig

def addObject(fig, shpObject, xrange, yrange):
    # 1: simple line
    ax = fig.add_subplot(111)
    plot_coords(ax, shpObject)
    plot_bounds(ax, shpObject)
    plot_line(ax, shpObject)
    #    ax.set_xlim(*xrange)
    #    ax.set_ylim(*yrange)
    #    ax.set_yticks(list(range(*yrange)) + [yrange[-1]])
    ax.set_aspect(1)


pyplot.show()

