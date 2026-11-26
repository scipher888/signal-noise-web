import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e27-factoring-count', 'artifact': 'episode', 'type': 'number', 'story': 'Google papers', 'quote': 'two theoretical factoring results, one randomized and one deterministic'}


def check(ctx):
    return ctx.require('framing', r'(?:two|2) (?:theoretical )?factoring (?:results|algorithms|papers).{0,100}one randomized.{0,30}one deterministic')


if __name__ == '__main__':
    run_cli(CLAIM, check)
