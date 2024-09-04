from typing import List

import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, find_peaks

from models import SensorData
from validator import Validator

fs = 100
nyquist = 0.5 * fs

lowpass_cutoff = 0.05 / nyquist
lowpass_order = 2
bandpass_cutoff = [0.5 / nyquist, 3 / nyquist]
bandpass_order = 4

low_b, low_a = butter(lowpass_order, lowpass_cutoff, btype="low", analog=False)
band_b, band_a = butter(bandpass_order, bandpass_cutoff, btype="band", analog=False)


def lowpass_filter(data):
    return filtfilt(low_b, low_a, data)


def bandpass_filter(data):
    return filtfilt(band_b, band_a, data)


def handle_data(data: List[SensorData]):
    validate = Validator()

    arr_red = [item.red for item in data]
    arr_ir = [item.ir for item in data]

    validate.red_ir(arr_red, arr_ir)

    isPhysiological = {"prop": "peak", "value": "0.8"}

    a = 1.6
    b = -35
    c = 113

    dc_ir = lowpass_filter(arr_ir)

    dc_red = lowpass_filter(arr_red)

    ac_ir = bandpass_filter(arr_ir)
    ac_red = bandpass_filter(arr_red)

    std_ac_ir = np.std(ac_ir)
    std_ac_red = np.std(ac_red)

    avg_dc_ir = np.mean(dc_ir)
    avg_dc_red = np.mean(dc_red)

    validate.avg_dc(avg_dc_ir)
    validate.avg_dc(avg_dc_red)

    pi_ir = std_ac_ir / avg_dc_ir
    pi_red = std_ac_red / avg_dc_red

    r = pi_red / pi_ir
    part1 = a * (r * r)
    part2 = b * r

    spo2 = part1 + part2 + c

    peaks, _ = find_peaks(ac_ir, distance=nyquist, prominence=0.4)

    validate.peaks(peaks)

    peak_intervals = np.diff(peaks) / fs  # Intervalos entre picos em segundos
    bpm = 60 / peak_intervals.mean()  # Batimentosbpm = 60 / peak_intervals.mean()

    validate.spo2(spo2)
    validate.bpm(bpm)

    return spo2, bpm, pi_ir * 100, isPhysiological
