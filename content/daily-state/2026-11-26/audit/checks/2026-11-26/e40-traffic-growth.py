import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e40-traffic-growth', 'artifact': 'episode', 'type': 'number', 'story': 'Rust migration', 'quote': 'Messages API traffic grew roughly eighteen hundred times since early 2024'}


def check(ctx):
    return ctx.require('anthropic', r'From early 2024 to fall 2026, API traffic grew roughly 1,800 times')


if __name__ == '__main__':
    run_cli(CLAIM, check)
