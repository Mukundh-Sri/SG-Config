from tkinter import *
from tkinter import ttk
import re
from headers import *


def check_float(newval):
    if newval == "":
        return True
    return (
        re.match(r"^\d*$", newval)
        is not None
        # and int(newval) <= 256000
        # and int(newval) >= 1000
    )


check_float_wrapper = (root.register(check_float), "%P")


def on_vco_start_change(event):
    start_freq[0].set(vco_start.get())


def on_stop_freq_change(event, i):
    if i < 7:
        start_freq[i + 1].set(stop_freq[i].get())


def on_duration_change(event, i):
    max_duration = 1310.7 if delay[i].get() else 655.35
    current_value = float(duration[i].get())

    if current_value > max_duration:
        duration[i].set(str(max_duration))


def on_next_ramp_select(event, i):
    next_ramp[i].set(next_ramp_combo[i].get())


def on_trigger_select(event, i):
    trigger[i].set(trigger_combo[i].current())

root.title("Configure Signal Generetor")

top = ttk.LabelFrame(root)
top.grid(column=1, row=1, columnspan=3, sticky="w")

icon = ttk.Frame(top)
icon.grid(column=0, row=1, sticky="w")

vco = ttk.LabelFrame(top, text="VCO Limits and Comparators")
vco.grid(column=1, row=1, sticky="e")

ramp = ttk.LabelFrame(root, text="Ramp Parameters", padding=(12, 12, 12, 12))
ramp.grid(column=1, row=7, sticky="w")

# Icon
Label(icon, image=logo, justify="center").grid(column=0, row=0, sticky="e")

# Start Frequency
ttk.Label(vco, text="VCO Start Frequency").grid(
    column=0, row=0, columnspan=2, pady=5, padx=5, sticky="e"
)
vco_start_entry = ttk.Entry(
    vco,
    textvariable=vco_start,
    validate="key",
    validatecommand=check_float_wrapper,
    width=8,
    justify="center",
)
vco_start_entry.bind("<FocusOut>", on_vco_start_change)
vco_start_entry.grid(column=4, row=0, columnspan=1, pady=5, padx=5)
ttk.Label(vco, text="MHz").grid(
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
    vco,
    textvariable=vco_high,
    validate="key",
    validatecommand=check_float_wrapper,
    width=8,
    justify="center",
).grid(column=4, row=1, columnspan=1, pady=5, padx=5)
ttk.Label(vco, text="MHz").grid(
    column=5, row=1, columnspan=1, pady=5, padx=5, sticky="w"
)

# Output Limit Low
ttk.Label(vco, text="Output Low Limit").grid(
    column=0, row=2, columnspan=2, pady=5, padx=5, sticky="e"
)
ttk.Entry(
    vco,
    textvariable=vco_low,
    validate="key",
    validatecommand=check_float_wrapper,
    width=8,
    justify="center",
).grid(column=4, row=2, columnspan=1, pady=5, padx=5)
ttk.Label(vco, text="MHz").grid(
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
    vco,
    textvariable=max_flag,
    validate="key",
    validatecommand=check_float_wrapper,
    width=8,
    justify="center",
).grid(column=4, row=4, columnspan=1, pady=5, padx=5)
ttk.Label(vco, text="MHz").grid(
    column=5, row=4, columnspan=1, pady=5, padx=5, sticky="w"
)

# Ramp Low Comparator
ttk.Label(vco, text="Min Ramp Flag").grid(
    column=0, row=5, columnspan=2, pady=5, padx=5, sticky="e"
)
ttk.Entry(
    vco,
    textvariable=min_flag,
    validate="key",
    validatecommand=check_float_wrapper,
    width=8,
).grid(column=4, row=5, columnspan=1, pady=5, padx=5)
ttk.Label(vco, text="MHz").grid(
    column=5, row=5, columnspan=1, pady=5, padx=5, sticky="w"
)

###########################################################################################

ttk.Checkbutton(ramp, text="Ramp Enable", variable=ramp_enable).grid(
    column=0, row=0, columnspan=9, pady=10, padx=5, sticky="n"
)

for i in range(0, 8):
    ttk.Label(ramp, text=ramp_label[i], justify="center").grid(
        row=1,
        column=i,
        pady=5,
        padx=15,
        sticky="ns",
    )

    ttk.Label(ramp, text=i).grid(row=i + 2, column=0, pady=5, padx=10, sticky="ns")

    start_freq_label[i] = ttk.Label(
        ramp,
        textvariable=start_freq[i],
    )
    start_freq_label[i].grid(row=i + 2, column=1, pady=5, padx=10, sticky="ns")

    stop_freq_entry[i] = ttk.Entry(
        ramp,
        textvariable=stop_freq[i],
        validate="key",
        validatecommand=check_float_wrapper,
        justify="center",
        width=8,
    )
    stop_freq_entry[i].grid(row=i + 2, column=2, pady=5, padx=10, sticky="ns")
    stop_freq_entry[i].bind(
        "<FocusOut>", lambda event, id=i: on_stop_freq_change(event, id)
    )

    duration_entry[i] = ttk.Entry(
        ramp,
        textvariable=duration[i],
        validate="key",
        validatecommand=check_float_wrapper,
        justify="center",
        width=8,
    )
    duration_entry[i].grid(row=i + 2, column=3, pady=5, padx=10, sticky="ns")
    duration_entry[i].bind(
        "<FocusOut>", lambda event, id=i: on_duration_change(event, id)
    )

    delay_box[i] = ttk.Checkbutton(
        ramp,
        variable=delay[i],
        command=lambda event, id=i: on_duration_change(event, id),
    )
    delay_box[i].grid(row=i + 2, column=4, pady=5, padx=10, sticky="ns")

    next_ramp_combo[i] = ttk.Combobox(
        ramp,
        values=ramp_options,
        state="readonly",
        width=2,
    )
    next_ramp_combo[i].grid(
        row=i + 2,
        column=5,
        pady=5,
        padx=10,
        sticky="ns",
    )
    next_ramp_combo[i].current(0)
    next_ramp_combo[i].bind(
        "<<ComboboxSelected>>", lambda event, id=i: on_next_ramp_select(event, id)
    )

    reset_box[i] = ttk.Checkbutton(
        ramp,
        variable=reset[i],
    )
    reset_box[i].grid(row=i + 2, column=6, pady=5, padx=10, sticky="ns")

    trigger_combo[i] = ttk.Combobox(
        ramp,
        values=trigger_options,
        state="readonly",
        width=10,
    )
    trigger_combo[i].grid(
        row=i + 2,
        column=7,
        pady=5,
        padx=10,
        sticky="ns",
    )
    trigger_combo[i].current(0)
    trigger_combo[i].bind(
        "<<ComboboxSelected>>", lambda event, id=i: on_trigger_select(event, id)
    )


root.mainloop()
