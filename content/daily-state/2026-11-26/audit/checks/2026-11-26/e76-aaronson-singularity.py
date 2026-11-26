import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e76-aaronson-singularity', 'artifact': 'episode', 'type': 'attribution', 'story': 'Aaronson Thanksgiving advice', 'quote': 'Aaronson wrote that this past week feels like the opening chapter of an AI singularity'}


def check(ctx):
    return ctx.require('framing', r'(?=.*Aaronson)(?=.*(?:past|last|this) week)(?=.*(?:opening chapter|beginning|start) of (?:an? |the )?AI singularity)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
