#!/usr/bin/env python3
"""YojanaSetu launcher — run from the ukis-yojanasetu folder.

    python3 run.py

Serves the app at http://127.0.0.1:8771
Stdlib only — no install step, no accounts, no network calls.
All data is SYNTHETIC DEMO DATA — no real citizen data.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.server import main  # noqa: E402

if __name__ == "__main__":
    main()
