from tkinter import *
from tkinter import ttk
import re

root = Tk()


ramp_label = [
    "Ramp\nNumber",
    "Start Frequency\n[MHz]",
    "Stop Frequency\n[MHz]",
    "Duration\n[us]",
    "Delay",
    "Next Ramp",
    "Reset",
    "Output\nTrigger",
]

ramp_options = [0, 1, 2, 3, 4, 5, 6, 7]

trigger_options = ["None", "Flag 1", "Flag 2", "Flag 1 & 2"]

button_display_text = " After completing the configuration\nclick Done to download the\nconfiguration CSV file"

# Logo
logo = PhotoImage(file="logo.png")

# VCO Config
vco_start = StringVar(value=10000)
vco_high = StringVar(value=12000)
vco_low = StringVar(value=9000)
max_flag = StringVar(value=9800)
min_flag = StringVar(value=9400)
file_name = StringVar(value="config")

# Ramp Config
ramp_enable = BooleanVar()
start_freq = [StringVar(value=vco_start.get()) for _ in range(0, 8)]
stop_freq = [StringVar(value=9000) for _ in range(0, 8)]
duration = [StringVar(value=655.35) for _ in range(0, 8)]
delay = [IntVar(value=0) for _ in range(8)]
next_ramp = [StringVar(value=i) for i in range(8)]
reset = [BooleanVar(value=False) for _ in range(8)]
trigger = [IntVar(value=0) for _ in range(8)]

# Ramp Config Dissplay Elements
start_freq_label = [ttk.Label() for i in range(0, 8)]
stop_freq_entry = [ttk.Entry() for i in range(0, 8)]
duration_entry = [ttk.Entry() for i in range(0, 8)]
delay_box = [ttk.Checkbutton() for i in range(0, 8)]
next_ramp_combo = [ttk.Combobox() for i in range(0, 8)]
reset_box = [ttk.Checkbutton() for i in range(0, 8)]
trigger_combo = [ttk.Combobox() for i in range(0, 8)]
