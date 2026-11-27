import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't17-benign-input', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Claude refusal behavior', 'quote': 'can trigger on benign work'}


def check(ctx):
    return ctx.require('framing', r'(?:classifier|refusal).*trigger on benign', note='Verify false-positive behavior in the docs.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
