from tkinter import *
from tkinter import ttk
import re

root = Tk()

# Ramp Labels
ramp_label = [
    "Ramp\nNumber",
    "Start Frequency\n[MHz]",
    "Stop Frequency\n[MHz]",
    "Duration\n[us]",
    "Delay",
    "Next Ramp",
    "Reset",
    "Trigger",
]

# VCO Config
vco_start = StringVar(value=10000)
vco_high = StringVar()
vco_low = StringVar()
max_flag = StringVar()
min_flag = StringVar()

# Ramp Config
ramp_enable = BooleanVar()
start_freq = [StringVar(value=vco_start.get()) for i in range(0, 8)]
stop_freq = [StringVar(value=vco_start.get()) for i in range(0, 8)]
duration = [StringVar(value=100) for i in range(0, 8)]
delay = [BooleanVar(value=False) for _ in range(8)]
next_ramp = [StringVar(value=0) for _ in range(8)]
reset = [BooleanVar(value=False) for _ in range(8)]
trigger = [IntVar(value=0) for _ in range(8)]

start_freq_label = [ttk.Label() for i in range(0, 8)]
stop_freq_entry = [ttk.Label() for i in range(0, 8)]
