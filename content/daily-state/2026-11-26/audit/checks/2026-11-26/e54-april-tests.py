import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e54-april-tests', 'artifact': 'episode', 'type': 'number', 'story': 'Production verification', 'quote': 'Rust passed ninety-eight percent of tests in April'}


def check(ctx):
    return ctx.support_or_contradict('anthropic', r'Rust API passed 98% of its tests in April', r'Rust API passed about 98% of its tests in April', 'Source qualifies the percentage as approximate.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
