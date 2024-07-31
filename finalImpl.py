import numpy as np
import pandas as pd
from scipy.signal import butter, filtfilt, find_peaks

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


def calc_mean_frequency(data):
    timestamps = pd.to_datetime(data, format="%Y-%m-%d %H:%M:%S:%f")

    time_diffs = np.diff(timestamps) / np.timedelta64(1, "s")
    frequencies = 1 / time_diffs
    mean_frequency = np.mean(frequencies)
    return mean_frequency


# ir red e timestamp array
def handle_data(data):
    a = 1.6
    b = -35
    c = 113

    dc_ir = lowpass_filter(data.ir)
    dc_red = lowpass_filter(data.red)

    ac_ir = bandpass_filter(data.ir)
    ac_red = bandpass_filter(data.red)

    std_ac_ir = np.std(ac_ir)
    std_ac_red = np.std(ac_red)

    avg_dc_ir = np.mean(dc_ir)
    avg_dc_red = np.mean(dc_red)

    pi_ir = std_ac_ir / avg_dc_ir
    pi_red = std_ac_red / avg_dc_red

    r = pi_red / pi_ir
    part1 = a * (r * r)
    part2 = b * r

    spo2 = part1 + part2 + c

    peaks, _ = find_peaks(ac_red, distance=70)
    first_peak = peaks[0]
    second_peak = peaks[1]
    peak_difference = second_peak - first_peak
    # calcular frequencia media das amostras
    peak_rate = 98.44 / peak_difference

    bpm = peak_rate * 60

    return spo2, bpm
