from consts import *
from headers import *
import csv

local_reg = list(REGISTER_MAP)


def split_to_8bit_hex(value):
    hex_str = f"{value:x}".zfill((len(f"{value:x}") + 1) // 2 * 2)
    return [hex_str[i : i + 2] for i in range(0, len(hex_str), 2)]


def dec_to_bin_str(value):
    return bin(int(value))[2:]


def twos_complement(value, n_bits):
    num = int(value)
    return num if num >= 0 else int(2**n_bits + num)


def set_reg(name):
    # Set VCO Freq
    local_reg[16] = (local_reg[16] & 0xFFFF00) + int(
        hex(int(vco_start.get()) // 100), 16
    )

    high = split_to_8bit_hex(
        twos_complement(
            ((int(vco_high.get()) - int(vco_start.get())) * 2**24) / 100, 33
        )
    )

    low = split_to_8bit_hex(
        twos_complement(((int(vco_low.get()) - int(vco_start.get())) * 2**24) / 100, 33)
    )
    cmp0 = split_to_8bit_hex(
        twos_complement(
            ((int(max_flag.get()) - int(vco_start.get())) * 2**24) / 100, 33
        )
    )
    cmp1 = split_to_8bit_hex(
        twos_complement(
            ((int(min_flag.get()) - int(vco_start.get())) * 2**24) / 100, 33
        )
    )

    for i in range(0, 4):
        local_reg[78 - i] = (local_reg[78 - i] & 0xFFFF00) + int(high[i], 16)
        local_reg[82 - i] = (local_reg[78 - i] & 0xFFFF00) + int(low[i], 16)
        local_reg[67 - i] = (local_reg[78 - i] & 0xFFFF00) + int(cmp1[i], 16)
        local_reg[63 - i] = (local_reg[78 - i] & 0xFFFF00) + int(cmp0[i], 16)

    # Set Ramp Properties
    if ramp_enable.get():
        local_reg[58] = local_reg[58] & 0xFFFFF0 + 0x1
        for i in range(0, 8):
            d = int(delay[i].get()) + 1
            # Increment
            inc = split_to_8bit_hex(
                twos_complement(
                    (
                        (
                            (
                                (int(stop_freq[i].get()) - int(start_freq[i].get()))
                                * d
                                * 2**24
                            )
                            / (float(duration[i].get()) * 10**4)
                        )
                    ),
                    30,
                )
            )

            # Padding last register with delay and fastlock
            inc[0] = hex(
                int("0x" + inc[0], 16) + int("0b" + str((d - 1) * 10 + 0) + "000000", 2)
            )[2:]

            print(inc)

            for i in range(0, 4):
                print(int(inc[3 - i], 16))
                local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + i] = (
                    local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + i] & 0xFFFF00
                ) + int(inc[3 - i], 16)

            # Length
            len = split_to_8bit_hex(int((float(duration[i].get()) * FPD // d)))
            local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 4] = (
                local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 4] & 0xFFFF00
            ) + int(len[1], 16)
            local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 5] = (
                local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 5] & 0xFFFF00
            ) + int(len[0], 16)

            # Auxilary Information
            aux = (
                "0b"
                + dec_to_bin_str(next_ramp[i].get())
                + "00"
                + dec_to_bin_str(reset[i].get())
                + dec_to_bin_str(trigger[i].get())
            )

            local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 6] = (
                local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 6] & 0xFFFF00
            ) + (int(aux, 2))

    print(name)

    with open(name, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Register", "Value (Hex)"])  # CSV header
        for index, value in enumerate(local_reg):
            writer.writerow(
                [f"R{index}", f"0x{value:06X}"]
            )  # Ensures 6-digit hex with uppercase
