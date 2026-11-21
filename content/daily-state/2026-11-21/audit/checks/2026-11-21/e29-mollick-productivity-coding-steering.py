import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e29-mollick-productivity-coding-steering', 'artifact': 'episode', 'type': 'attribution', 'story': 'AI task-horizon analysis', 'quote': "As Wharton's Ethan Mollick noted today, AI is already delivering massive productivity on well-specified coding tasks, or whenever a human is steering it."}


def check(ctx):
    return ctx.require('emollick', r'Wharton professor', r'well-specified work', r'Occasional guidance.*enormous productivity gains')


if __name__ == '__main__':
    run_cli(CLAIM, check)
