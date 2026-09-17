# Adaptive Noise Cancellation (ANC)

A Python toolkit for real-time and offline adaptive noise cancellation using classical adaptive filter algorithms — LMS, NLMS, and RLS.

## Overview

This project demonstrates **Active/Adaptive Noise Cancellation** by training adaptive filters to identify and suppress periodic interference (e.g. electrical hum at 50/60 Hz and harmonics) from an audio signal. It ships with two modes:

- **Offline demo** — processes a synthetically generated noisy signal and benchmarks all three filters side-by-side.
- **Live demo** — captures microphone input in real-time, auto-detects hum frequencies, and applies an adaptive filter, with a GUI for switching between algorithms.

## Algorithms

All filters are implemented from scratch in `anc/filters.py` using NumPy — no external DSP libraries required.

| Filter | Class | Key Parameters | Characteristics |
|--------|-------|----------------|-----------------|
| LMS | `LMSFilter` | `order=64`, `mu=0.005` | Simple, robust, slow convergence |
| NLMS | `NLMSFilter` | `order=64`, `mu=0.5` | Normalised step size, faster convergence |
| RLS | `RLSFilter` | `order=16`, `lam=0.999`, `delta=100.0` | Fastest convergence, higher compute cost |

## Project Structure

```
.
├── main.py                      # Entry point (CLI)
├── anc/                         # Core package
│   ├── __init__.py
│   ├── filters.py               # LMS, NLMS, RLS filter implementations
│   ├── signal_utils.py          # SNR/MSE metrics, hum detection, audio I/O
│   ├── offline_demo.py          # Batch benchmark with matplotlib plots
│   └── live_demo.py             # Real-time Tkinter GUI with sounddevice
├── scripts/
│   └── plot_frequency_analysis.py  # FFT spectrum comparison figure
├── docs/
│   └── Project_Report.pdf
├── outputs/                     # Generated WAV files & figures (gitignored)
├── requirements.txt
└── README.md
```

## Installation

**Python 3.9+ recommended.**

```bash
pip install -r requirements.txt
```

Dependencies:

- `numpy` — array maths and FFT
- `scipy` — signal processing utilities
- `matplotlib` — offline plotting
- `sounddevice` — real-time audio I/O (live mode)
- `soundfile` — WAV file read/write

## Usage

### Offline demo

Generates a synthetic test signal (300 Hz + 800 Hz speech tone buried under 50 Hz + 150 Hz hum and thermal noise), runs all three filters, prints SNR/MSE metrics, saves output WAV files (`outputs/`), and displays a comparison plot.

```bash
python main.py
```

Example output:

```
Detected Hum Frequencies: [50.0, 150.0]

Input SNR: -4.83 dB

LMS
SNR : 8.21 dB
MSE : 0.007314

NLMS
SNR : 9.05 dB
MSE : 0.006198

RLS
SNR : 11.47 dB
MSE : 0.004521
```

### Live demo (microphone)

Launches a Tkinter GUI that streams microphone audio through the selected adaptive filter in real-time.

```bash
python main.py --live
```

GUI controls:

- **Dropdown** — switch between LMS / NLMS / RLS on the fly
- **START** — begin audio stream
- **STOP** — end stream and save output to a timestamped WAV file in `outputs/` (`anc_output_YYYYMMDD_HHMMSS.wav`)

> **Note:** The live demo requires a working microphone and audio output device. Default sample rate is 16 kHz with 512-sample blocks.

### Frequency analysis figure

Generates `outputs/frequency_comparison.png`, comparing the noise spectra before and after ANC (used in the project report).

```bash
python scripts/plot_frequency_analysis.py
```

## How It Works

1. **Hum detection** — `detect_hum_frequencies()` computes the FFT of the incoming audio and checks a list of candidate frequencies (50, 60 Hz) against a configurable dB threshold.
2. **Reference generation** — A synthetic sinusoidal reference signal is synthesised at the detected frequencies to serve as the adaptive filter's input.
3. **Adaptive filtering** — The filter minimises the error between the reference (estimated noise) and the primary (noisy) signal, producing a cleaned output.
4. **Metrics** — SNR (dB) and MSE are computed against the known clean signal (offline mode only).

## Output Files

Processed audio is saved as 32-bit float WAV files inside `outputs/`. These are excluded from version control via `.gitignore`.

## License

MIT