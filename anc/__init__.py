"""Adaptive Noise Cancellation (ANC) package.

Core modules:
- filters.py      : LMS, NLMS, RLS adaptive filter implementations
- signal_utils.py : SNR/MSE metrics, hum detection, audio I/O
- offline_demo.py : batch benchmark with matplotlib plots
- live_demo.py    : real-time Tkinter GUI with sounddevice
"""