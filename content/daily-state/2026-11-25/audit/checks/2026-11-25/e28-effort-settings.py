import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e28-effort-settings', 'artifact': 'episode', 'type': 'comparison', 'story': "Humanity's First Exam", 'quote': "at a higher reasoning setting than Google's Gemini 4 Neon"}


def check(ctx):
    return ctx.require('kaggle', r'🥇\s*GPT-\s*6\.2 Astra \(xhigh\)', r'🥉\s*Gemini 4 Neon \(high\)', note='Comparison of setting labels in this run, not calibrated compute.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
