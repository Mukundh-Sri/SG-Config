from consts import *
from headers import *
import csv

local_reg = list(REGISTER_MAP)


def split_to_8bit_hex(value):
    hex_str = f"{value:x}".zfill((len(f"{value:x}") + 1) // 2 * 2)
    hex_list = [hex_str[i : i + 2] for i in range(0, len(hex_str), 2)]

    while len(hex_list) < 4:
        hex_list.insert(0, "00")

    return hex_list[-4:]


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
            ((int(cmp0_flag.get()) - int(vco_start.get())) * 2**24) / 100, 33
        )
    )

    cmp1 = split_to_8bit_hex(
        twos_complement(
            ((int(cmp1_flag.get()) - int(vco_start.get())) * 2**24) / 100, 33
        )
    )

    sign = int(
        (
            "0b000"
            + ("0" if int(vco_high.get()) > int(vco_start.get()) else "1")
            + ("0" if int(vco_low.get()) > int(vco_start.get()) else "1")
            + "0"
            + ("0" if int(cmp1_flag.get()) > int(vco_start.get()) else "1")
            + ("0" if int(cmp0_flag.get()) > int(vco_start.get()) else "1")
        ),
        2,
    )

    local_reg[70] = (local_reg[70] & 0xFFFF00) + sign

    for i in range(0, 4):
        local_reg[78 - i] = (local_reg[78 - i] & 0xFFFF00) + int(low[i], 16)
        local_reg[82 - i] = (local_reg[82 - i] & 0xFFFF00) + int(high[i], 16)
        local_reg[68 - i] = (local_reg[68 - i] & 0xFFFF00) + int(cmp1[i], 16)
        local_reg[63 - i] = (local_reg[63 - i] & 0xFFFF00) + int(cmp0[i], 16)

    # Set Ramp Properties
    if ramp_enable.get():
        local_reg[58] = (local_reg[58] & 0xFFFFF0) + 0x1
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

            for j in range(0, 4):
                local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + j] = (
                    local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + j] & 0xFFFF00
                ) + int(inc[3 - j], 16)

            # Length
            length = split_to_8bit_hex(int((float(duration[i].get()) * FPD // d)))
            local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 4] = (
                local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 4] & 0xFFFF00
            ) + int(length[3], 16)
            local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 5] = (
                local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 5] & 0xFFFF00
            ) + int(length[2], 16)

            # Auxilary Information

            trig = (
                dec_to_bin_str(trigger[i].get())
                if len(dec_to_bin_str(trigger[i].get())) == 2
                else ("0" + dec_to_bin_str(trigger[i].get()))
            )
            aux = (
                "0b"
                + dec_to_bin_str(next_ramp[i].get())
                + "00"
                + dec_to_bin_str(reset[i].get())
                + trig
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
