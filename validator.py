import numpy as np


class Validator:
    def __init__(self):
        pass

    def red_ir(self, arr_red, arr_ir):
        MAX_RED_MEAN = 600000
        MIN_RED_MEAN = 50000

        MAX_IR_MEAN = 500000
        MIN_IR_MEAN = 15000

        arr_ir_mean = np.mean(arr_ir)
        arr_red_mean = np.mean(arr_red)

        red_invalid = arr_red_mean > MAX_RED_MEAN or arr_red_mean < MIN_RED_MEAN

        ir_invalid = arr_ir_mean > MAX_IR_MEAN or arr_ir_mean < MIN_IR_MEAN

        if red_invalid and ir_invalid:
            raise ValueError("RED and IR data out of range")
        elif red_invalid:
            raise ValueError("RED data out of range")
        elif ir_invalid:
            raise ValueError("IR data out of range")

        return

    def avg_dc(self, dc):
        if dc == 0:
            raise ValueError("Average DC value is 0")
        return

    def peaks(self, peaks):
        MIN_PEAK_AMOUNT = 2
        if len(peaks) <= MIN_PEAK_AMOUNT:
            raise ValueError("amount of peaks is less than 2")
        return

    def spo2(self, value):
        MIN_SPO2 = 60
        MAX_SPO2 = 110

        if value > MAX_SPO2 or value < MIN_SPO2:
            raise ValueError("spo2 out of range")
        return

    def bpm(self, value):
        MIN_BPM = 40
        MAX_BPM = 120

        if value > MAX_BPM or value < MIN_BPM:
            raise ValueError("bps out of range")
        return
