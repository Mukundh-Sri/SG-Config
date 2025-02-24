from consts import *
from headers import *

local_reg = list(REGISTER_MAP)


def split_to_8bit_hex(value):
    hex_str = f"{value:x}".zfill((len(f"{value:x}") + 1) // 2 * 2)
    return [hex_str[i : i + 2] for i in range(0, len(hex_str), 2)]


def dec_to_bin_str(value):
    return bin(int(value))[2:]


def twos_complement(value):
    num = int(value)
    return num if num >= 0 else int(2**30 + num)


def set_reg():

    # Set VCO Freq
    local_reg[16] = (local_reg[16] & 0xFFFF00) + int(
        hex(int(vco_start.get()) // 100), 16
    )

    if True:
        for i in range(0, 8):
            d = int(delay[i].get()) + 1

            # Increment
            inc = split_to_8bit_hex(
                twos_complement(
                    (
                        (
                            (int(stop_freq[i].get()) - int(start_freq[i].get()))
                            * d
                            * 2**24
                        )
                        / (float(duration[i].get()) * 10**4)
                    )
                )
            )

            # Padding last register with delay and fastlock

            inc[0] = hex(
                int("0x" + inc[0], 16) + int("0b" + str(d * 10 + 0) + "000000", 2)
            )[2:]

            local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 0] = (
                local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 0] & 0xFFFF00
            ) + int(inc[3], 16)
            local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 1] = (
                local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 1] & 0xFFFF00
            ) + int(inc[2], 16)
            local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 2] = (
                local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 2] & 0xFFFF00
            ) + int(inc[1], 16)
            local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 3] = (
                local_reg[RAMP_REG_START + i * RAMP_REG_NEXT + 3] & 0xFFFF00
            ) + int(inc[0], 16)

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


set_reg()
