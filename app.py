from tkinter import *
from tkinter import ttk
import re

root = Tk()


def check_float(newval):
    if newval == "":
        return True
    return re.match(r"^\d*\.?\d*$", newval) is not None and float(newval) <= 256


check_float_wrapper = (root.register(check_float), "%P")

vco_start = StringVar()
vco_high = StringVar()
vco_low = StringVar()
max_flag = StringVar()
min_flag = StringVar()
ramp_enable = BooleanVar()
stop_freq = [vco_start, -1, -1, -1, -1, -1, -1, -1]
start_freq = [vco_start, stop_freq[0:6]]

vco = ttk.LabelFrame(root, text="VCO Limits and Comparators", padding=(12, 12, 12, 12))
vco.grid(column=0, row=0, sticky="w")

ramp = ttk.LabelFrame(root, text="Ramp Parameters", padding=(12, 12, 12, 12))
ramp.grid(column=0, row=6, sticky="w")

# Start Frequency
ttk.Label(vco, text="VCO Start Frequency").grid(
    column=0, row=0, columnspan=2, pady=5, padx=5, sticky="e"
)
ttk.Entry(
    vco, textvariable=vco_start, validate="key", validatecommand=check_float_wrapper
).grid(column=4, row=0, columnspan=1, pady=5, padx=5)
ttk.Label(vco, text="GHz").grid(
    column=5, row=0, columnspan=1, pady=5, padx=5, sticky="w"
)

ttk.Separator(vco, orient=HORIZONTAL).place(
    relx=0, rely=0.20, relwidth=1.5, relheight=1
)

# Output Limit High
ttk.Label(vco, text="Output High Limit").grid(
    column=0, row=1, columnspan=2, pady=5, padx=5, sticky="e"
)
ttk.Entry(
    vco, textvariable=vco_high, validate="key", validatecommand=check_float_wrapper
).grid(column=4, row=1, columnspan=1, pady=5, padx=5)
ttk.Label(vco, text="GHz").grid(
    column=5, row=1, columnspan=1, pady=5, padx=5, sticky="w"
)

# Output Limit Low
ttk.Label(vco, text="Output Low Limit").grid(
    column=0, row=2, columnspan=2, pady=5, padx=5, sticky="e"
)
ttk.Entry(
    vco, textvariable=vco_low, validate="key", validatecommand=check_float_wrapper
).grid(column=4, row=2, columnspan=1, pady=5, padx=5)
ttk.Label(vco, text="GHz").grid(
    column=5, row=2, columnspan=1, pady=5, padx=5, sticky="w"
)

ttk.Separator(vco, orient=HORIZONTAL).place(
    relx=0, rely=0.60, relwidth=1.5, relheight=1
)
# Ramp High Comparator
ttk.Label(vco, text="Max Ramp Flag").grid(
    column=0, row=4, columnspan=2, pady=5, padx=5, sticky="e"
)
ttk.Entry(
    vco, textvariable=max_flag, validate="key", validatecommand=check_float_wrapper
).grid(column=4, row=4, columnspan=1, pady=5, padx=5)
ttk.Label(vco, text="GHz").grid(
    column=5, row=4, columnspan=1, pady=5, padx=5, sticky="w"
)

# Ramp Low Comparator
ttk.Label(vco, text="Min Ramp Flag").grid(
    column=0, row=5, columnspan=2, pady=5, padx=5, sticky="e"
)
ttk.Entry(
    vco, textvariable=min_flag, validate="key", validatecommand=check_float_wrapper
).grid(column=4, row=5, columnspan=1, pady=5, padx=5)
ttk.Label(vco, text="GHz").grid(
    column=5, row=5, columnspan=1, pady=5, padx=5, sticky="w"
)

###########################################################################################

ttk.Checkbutton(ramp, text="Ramp Enable", variable=ramp_enable).grid(
    column=0, row=0, columnspan=5, pady=5, padx=5, sticky="n"
)

root.mainloop()
