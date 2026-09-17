from __future__ import annotations

import numpy as np
import soundfile as sf
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"


def snr_db(clean: np.ndarray, signal: np.ndarray) -> float:
    noise_power = float(np.mean((signal - clean) ** 2)) + 1e-12
    signal_power = float(np.mean(clean ** 2)) + 1e-12
    return 10.0 * np.log10(signal_power / noise_power)


def mse_metric(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((a - b) ** 2))


# Only true mains hum frequencies (50 Hz for India/EU, 60 Hz for US).
# Higher harmonics (100, 120, 150 Hz etc.) were causing false positives
# on laptop mics because broadband background noise has energy at those
# frequencies too, making every block detect everything.
_DEFAULT_CANDIDATES = [50, 60]


def detect_hum_frequencies(
    audio: np.ndarray,
    fs: int,
    candidates=None,
    threshold_db: float = -5.0,  # raised from -10.0 — only detect dominant spikes
    bin_half_width: int = 2,
):
    """
    Detect electrical hum frequencies in an audio signal via FFT peak analysis.

    Parameters
    ----------
    audio        : input audio frame (numpy array)
    fs           : sample rate in Hz
    candidates   : list of candidate hum frequencies to check (Hz)
    threshold_db : minimum peak level relative to spectrum max to count as hum.
                   -5.0 dB means a candidate must be within 5 dB of the
                   strongest peak in the entire spectrum to be detected.
                   This is strict enough to ignore broadband noise floor
                   energy on laptop microphones, which was causing all
                   candidate frequencies to be detected simultaneously.
    bin_half_width: number of FFT bins either side of target to search for peak
    """
    if candidates is None:
        candidates = _DEFAULT_CANDIDATES

    N = len(audio)

    if N < 512:
        return []

    window = np.hanning(N)

    spectrum = np.abs(np.fft.rfft(audio * window))

    freqs = np.fft.rfftfreq(N, d=1.0 / fs)

    peak = float(spectrum.max()) + 1e-12

    spec_db = 20.0 * np.log10(spectrum / peak + 1e-12)

    detected = []

    for target_hz in candidates:

        if target_hz >= fs / 2.0:
            break

        idx = int(np.argmin(np.abs(freqs - target_hz)))

        lo = max(0, idx - bin_half_width)
        hi = min(len(spec_db) - 1, idx + bin_half_width)

        peak_val = float(spec_db[lo: hi + 1].max())

        if peak_val > threshold_db:
            detected.append(float(target_hz))

    return detected


def save_audio(audio: np.ndarray, fs: int, prefix: str = "anc") -> str:

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"{prefix}_{timestamp}.wav"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    path = OUTPUT_DIR / filename

    sf.write(path, audio.astype(np.float32), fs)

    return str(path)