import matplotlib as mpl
import matplotlib.pyplot as plt
from math import sin, sqrt
import gui
import numpy as np

# Set style
text_color = '#d8d9db'
passive_text_color = '#58595b'
mpl.rcParams['text.color'] = text_color
mpl.rcParams['axes.labelcolor'] = text_color
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color
mpl.rcParams['axes.edgecolor'] = text_color
colormaps = [mpl.cm.viridis, mpl.cm.jet, mpl.cm.seismic, mpl.cm.Spectral, mpl.cm.coolwarm, mpl.cm.gist_rainbow, mpl.cm.gnuplot2, mpl.cm.turbo, mpl.cm.bwr, mpl.cm.magma, mpl.cm.plasma, mpl.cm.cividis, mpl.cm.inferno, mpl.cm.twilight_shifted]

class wave:
    def __init__(self, x, y, omega=1, smax=1, phi=0, velocity=1, start_time=0):
        self.omega = omega
        self.smax = smax
        self.phi = phi
        self.pos = (x, y)
        self.velocity = velocity
        self.start_time = start_time

    def set_x(self, val):
        self.pos = (val, self.pos[1])

    def set_y(self, val):
        self.pos = (self.pos[0], val)

    def set_phi(self, val):
        self.phi = val

    def set_smax(self, val):
        self.smax = val

    def set_start_time(self, val):
        self.start_time = val

    def set_velocity(self, val):
        self.velocity = val if val != 0 else 0.0

    def set_omega(self, val):
        self.omega = val

    def calc(self, x_start, y_start, x_end, y_end, time, d):
        # d: how fine the calculations will be
        x_start *= d; y_start *= d; x_end *= d; y_end *= d
        # Calculate matrix
        mat = [[x/d, y/d, self.calc_point(x/d, y/d, time)] for x in range(x_start, x_end) for y in range(y_start, y_end)]
        return mat

    def calc_point(self, x, y, time: int):
        # Distance to point from wave origin
        distance = pythagoras(self.pos, (x,y))
        # Wave hasn't reached point yet
        if distance > (time-self.start_time)*self.velocity: return 0
        # Calculate value for point
        return self.smax*sin(self.omega*(time-distance/self.velocity)+self.phi)


def plot_data(ax, matrices, fig=None, colormap=0):
    # Clear ax
    ax.clear()

    # Add all matrices together
    matrix = matrices[0]
    for _matrix in matrices[1:]:
        matrix[:, 2] += _matrix[:, 2]
    # Seperate x,y and z values
    Xs = matrix[:, 0]
    Ys = matrix[:, 1]
    Zs = matrix[:, 2]

    ax.tricontourf(Xs, Ys, Zs, 20, norm=mpl.colors.CenteredNorm(), cmap=colormaps[colormap])

    if fig:
        fig.canvas.draw()


def show(matrices, params):
    # Fig that everything will be placed in
    fig: plt.figure = plt.figure(layout='tight')

    # style
    fig.patch.set_facecolor('#1c1e21')

    # Plot data on axis
    ax = fig.add_axes([0.15, 0, 0.85, 1])
    plot_data(ax, matrices, colormap=params[7])

    # Add time slider
    redraw = lambda val: plot_data(ax, np.array([wave.calc(params[1], params[2], params[3], params[4], time_slider.val, params[6]) for wave in params[0]]), fig, params[7])
    ax_time = fig.add_axes([0.025, 0.1, 0.02, 0.64])
    time_slider = plt.Slider(
        ax=ax_time,
        label="t (s)",
        valmin=0,
        valmax=50,
        valinit=params[5],
        orientation="vertical",
        handle_style={'facecolor': '#3c4caa', 'edgecolor': '#3c4caa', 'size': 12}
    )
    time_slider.on_changed(redraw)
    # style of slider
    time_slider.hline.set_visible(False)
    time_slider.poly.set_facecolor(text_color)
    time_slider.track.set_facecolor(passive_text_color)

    plt.show()

def show_waves(waves, x_start, y_start, x_end, y_end, time, d, colormap=0):
    if isinstance(waves, wave): waves = [waves]
    matrices = np.array([wave.calc(x_start, y_start, x_end, y_end, time, d) for wave in waves])
    show(matrices=matrices, params=[waves, x_start, y_start, x_end, y_end, time, d, colormap])


def pythagoras(pos1, pos2):
    return sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)


def example_func():
    """
        Example method to showcase module funtionality
    """
    w1 = wave(x=10, y=10, omega=3, smax=10, phi=1, velocity=1, start_time=0)
    w2 = wave(x=-10, y=-10, omega=3, smax=10, phi=1, velocity=1, start_time=0)
    show_waves(waves=[w1, w2], x_start=-30, y_start=-30, x_end=30, y_end=30, time=20, d=2)


if __name__ == '__main__':
    # Open GUI
    gui.init()