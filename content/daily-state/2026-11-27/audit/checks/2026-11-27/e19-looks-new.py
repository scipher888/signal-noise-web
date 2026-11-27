import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e19-looks-new', 'artifact': 'episode', 'type': 'opinion', 'story': 'METR chart debate', 'quote': 'making a quick commentary look like a new research finding'}


def check(ctx):
    return ctx.need('bethmaybarnes', ctx.find('bethmaybarnes', r'foreseeable that having this graph as the headline figure'), 'Interpretation of reader perception.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
