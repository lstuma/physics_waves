import tkinter as ctk
from wavy import *
from threading import Thread
import customtkinter as ctk

# Set customtkinter theme
ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


object_tracker = []
wave_tracker = []

x_start = -10
x_end = 10
y_start = -10
y_end = 10
time = 10
precision = 2

def generate(event=None):
    if len(wave_tracker) >= 1:
        th = Thread(target=show_waves, args=[wave_tracker, x_start, y_start, x_end, y_end, time, precision])
        th.run()

def set_time(val):
    global time
    time = val

def set_x_start(val):
    global x_start
    x_start = int(val)
def set_y_start(val):
    global y_start
    y_start = int(val)
def set_x_end(val):
    global x_end
    x_end = int(val)
def set_y_end(val):
    global y_end
    y_end = int(val)

def set_precision(val):
    global precision
    precision = int(val)

def callcenter(callbacks: list, event=None):
    for callback in callbacks: callback(event)

def callcenter_builder(callbacks):
    if not isinstance(callbacks, list): return callbacks
    return lambda event: [callback(event) for callback in callbacks]

def init():
    global  root
    root = ctk.CTk()
    root.wm_title("Wavy: Physics Wave Editor")
    root.resizable(width=False, height=False)

    # Area for user controls
    global controls_frame
    controls_frame = ctk.CTkFrame(root, width=400, height=500)
    controls_frame.grid(column=1, row=0, sticky='ne')

    # Frame for 'Add Wave' and 'Generate' button
    sframe = ctk.CTkFrame(controls_frame)
    sframe.pack(side='top', anchor='nw', padx=5, pady=5, fill='x')
    # Wave Button for adding waves
    btn = ctk.CTkButton(sframe, text="Add Wave", width=150)
    btn.pack(side='left', anchor='nw', padx=10, pady=10)
    btn.bind('<Button-1>', add_wave)
    object_tracker.append(btn)
    # Image Button for opening mpl with waves
    btn = ctk.CTkButton(sframe, text="Generate", width=150)
    btn.bind('<Button-1>', generate)
    btn.pack(side='right', anchor='ne', padx=10, pady=10)
    object_tracker.append(btn)

    # Frame for configuration sliders
    sframe = ctk.CTkFrame(controls_frame)
    sframe.pack(side='top', anchor='nw', padx=5, pady=5, fill='x')

    # min_X
    sl = lambda val: minx_slider_label.configure(text=f'Min X (m) [{round(val, 1)}]')
    minx_slider = ctk.CTkSlider(sframe, from_=-50, to=-1, command=callcenter_builder([set_x_start, sl]))
    minx_slider.pack(side='top', fill='x')
    minx_slider.set(-10)
    object_tracker.append(minx_slider)
    minx_slider_label = ctk.CTkLabel(sframe, text="Min X (m) [-10]")
    minx_slider_label.pack(side='top', fill='x')
    object_tracker.append(minx_slider_label)
    # max_X
    sl = lambda val: maxx_slider_label.configure(text=f'Max X (m) [{round(val, 1)}]')
    maxx_slider = ctk.CTkSlider(sframe, from_=1, to=50, command=callcenter_builder([set_x_end, sl]))
    maxx_slider.pack(side='top', fill='x')
    maxx_slider.set(10)
    object_tracker.append(maxx_slider)
    maxx_slider_label = ctk.CTkLabel(sframe, text="Max X (m) [10]")
    maxx_slider_label.pack(side='top', fill='x')
    object_tracker.append(maxx_slider_label)

    # min_Y
    sl = lambda val: miny_slider_label.configure(text=f'Min Y (m) [{round(val, 1)}]')
    miny_slider = ctk.CTkSlider(sframe, from_=-50, to=-1, command=callcenter_builder([set_y_start, sl]))
    miny_slider.pack(side='top', fill='x')
    miny_slider.set(-10)
    object_tracker.append(miny_slider)
    miny_slider_label = ctk.CTkLabel(sframe, text="Min Y (m) [-10]")
    miny_slider_label.pack(side='top', fill='x')
    object_tracker.append(miny_slider_label)
    # max_Y
    sl = lambda val: maxy_slider_label.configure(text=f'Max Y (m) [{round(val, 1)}]')
    maxy_slider = ctk.CTkSlider(sframe, from_=1, to=50, command=callcenter_builder([set_y_end, sl]))
    maxy_slider.pack(side='top', fill='x')
    maxy_slider.set(10)
    object_tracker.append(maxy_slider)
    maxy_slider_label = ctk.CTkLabel(sframe, text="Max Y (m) [10]")
    maxy_slider_label.pack(side='top', fill='x')
    object_tracker.append(maxy_slider_label)

    # time
    sl = lambda val: time_slider_label.configure(text=f'Time (s) [{round(val, 1)}]')
    time_slider = ctk.CTkSlider(sframe, from_=0, to=100, command=callcenter_builder([set_time, sl]))
    time_slider.pack(side='top', fill='x')
    time_slider.set(10)
    object_tracker.append(miny_slider)
    time_slider_label = ctk.CTkLabel(sframe, text="Time (s) [10]")
    time_slider_label.pack(side='top', fill='x')
    object_tracker.append(time_slider_label)

    # precision
    sl = lambda val: precision_slider_label.configure(text=f'Precision (dots per m) [{round(val)}]')
    precision_slider = ctk.CTkSlider(sframe, from_=1, to=10, command=callcenter_builder([set_precision, sl]))
    precision_slider.pack(side='top', fill='x')
    precision_slider.set(2)
    object_tracker.append(miny_slider)
    precision_slider_label = ctk.CTkLabel(sframe, text="Precision (dots per m) [2]")
    precision_slider_label.pack(side='top', fill='x')
    object_tracker.append(precision_slider_label)


    # Area for configuring waves
    global wave_frame
    wave_frame = ctk.CTkScrollableFrame(root, width=800, height=500)
    wave_frame.grid(column=0, row=0, sticky='ne')
    add_wave()
    root.mainloop()


def add_wave(event=None):
    global wave_frame
    # Create wave with default parameters
    wavy = wave(x=0, y=0, omega=1, smax=2, phi=0, velocity=1, start_time=0)
    wave_tracker.append(wavy)
    # Add list with this wave to object tracker to avoid garbage collection (THANKS PYTHON!??!?!?!)
    object_tracker.append([])
    # Create frame for buttons
    frame = ctk.CTkFrame(wave_frame)
    frame.pack(side='top', anchor='nw')
    object_tracker[-1].append(frame)

    # Create sliders for wave controls

    sframe = ctk.CTkFrame(frame)
    sframe.pack(side='left', anchor='nw')
    ssframe = ctk.CTkFrame(sframe)
    ssframe.pack(side='top', anchor='nw')
    # Lambda for adjusting values
    l = lambda val: wavy.set_x(int(val))
    sl = lambda val: x_slider_label.configure(text=f'X POS [{round(val, 1)}]')
    x_slider = ctk.CTkSlider(ssframe, from_=-50, to=50, command=callcenter_builder([l, sl]))
    x_slider.pack(side='top')
    x_slider.set(0)
    x_slider_label = ctk.CTkLabel(ssframe, text="X POS")
    x_slider_label.pack(side='top')

    ssframe = ctk.CTkFrame(sframe)
    ssframe.pack(side='top', anchor='nw')
    # Lambda for adjusting values
    l = lambda val: wavy.set_y(int(val))
    sl = lambda val: y_slider_label.configure(text=f'Y POS [{round(val, 1)}]')
    y_slider = ctk.CTkSlider(ssframe, from_=-50, to=50, command=callcenter_builder([l, sl]))
    y_slider.pack(side='top')
    y_slider.set(0)
    y_slider_label = ctk.CTkLabel(ssframe, text="Y POS")
    y_slider_label.pack(side='top')

    sframe = ctk.CTkFrame(frame)
    sframe.pack(side='left', anchor='nw')
    ssframe = ctk.CTkFrame(sframe)
    ssframe.pack(side='top', anchor='nw')
    # Lambda for adjusting values
    l = lambda val: wavy.set_omega(int(val))
    sl = lambda val: omega_slider_label.configure(text=f'OMEGA [{round(val, 1)}]')
    omega_slider = ctk.CTkSlider(ssframe, from_=-5, to=5, command=callcenter_builder([l, sl]))
    omega_slider.pack(side='top')
    omega_slider.set(1)
    omega_slider_label = ctk.CTkLabel(ssframe, text="OMEGA")
    omega_slider_label.pack(side='top')

    ssframe = ctk.CTkFrame(sframe)
    ssframe.pack(side='top', anchor='nw')
    # Lambda for adjusting values
    l = lambda val: wavy.set_phi(int(val))
    sl = lambda val: phi_slider_label.configure(text=f'PHI [{round(val, 1)}]')
    phi_slider = ctk.CTkSlider(ssframe, from_=-5, to=5, command=callcenter_builder([l, sl]))
    phi_slider.pack(side='top')
    phi_slider.set(0)
    phi_slider_label = ctk.CTkLabel(ssframe, text="PHI")
    phi_slider_label.pack(side='top')

    sframe = ctk.CTkFrame(frame)
    sframe.pack(side='left', anchor='nw')
    ssframe = ctk.CTkFrame(sframe)
    ssframe.pack(side='top', anchor='nw')
    # Lambda for adjusting values
    l = lambda val: wavy.set_smax(int(val))
    sl = lambda val: smax_slider_label.configure(text=f'Smax (m) [{round(val, 1)}]')
    smax_slider = ctk.CTkSlider(ssframe, from_=0, to=10, command=callcenter_builder([l, sl]))
    smax_slider.pack(side='top')
    smax_slider.set(2)
    smax_slider_label = ctk.CTkLabel(ssframe, text="Smax (m)")
    smax_slider_label.pack(side='top')

    ssframe = ctk.CTkFrame(sframe)
    ssframe.pack(side='top', anchor='nw')
    # Lambda for adjusting values
    l = lambda val: wavy.set_velocity(int(val))
    sl = lambda val: velocity_slider_label.configure(text=f'Velocity (m/s) [{round(val, 1)}]')
    velocity_slider = ctk.CTkSlider(ssframe, from_=0, to=10, command=callcenter_builder([l, sl]))
    velocity_slider.pack(side='top')
    velocity_slider.set(1)
    velocity_slider_label = ctk.CTkLabel(ssframe, text="Velocity (m/s)")
    velocity_slider_label.pack(side='top')

    sframe = ctk.CTkFrame(frame)
    sframe.pack(side='left', anchor='nw')
    ssframe = ctk.CTkFrame(sframe)
    ssframe.pack(side='top', anchor='nw')
    # Lambda for adjusting values
    l = lambda val: wavy.set_start_time(int(val))
    sl = lambda val: start_slider_label.configure(text=f'Start Time (s) [{round(val, 1)}]')
    start_slider = ctk.CTkSlider(ssframe, from_=-0, to=20, command=callcenter_builder([l, sl]))
    start_slider.pack(side='top')
    start_slider.set(0)
    start_slider_label = ctk.CTkLabel(ssframe, text="Start Time (s)")
    start_slider_label.pack(side='top')

    ssframe = ctk.CTkFrame(sframe)
    ssframe.pack(side='top', anchor='nw')
    # Lambda for deleting wave
    delwave = lambda event: delete_wave(len(wave_tracker)-1, len(object_tracker)-1)
    btn = ctk.CTkButton(ssframe, text="X", width=1000)
    btn.configure(fg_color='#d91a33', hover_color='#b31933')
    btn.pack(side='top', fill='x')
    btn.bind('<Button-1>', delwave)

def delete_wave(wave_index, object_index):
    wave_tracker.pop(wave_index)
    object_tracker[object_index][0].destroy()
    object_tracker.pop(object_index)