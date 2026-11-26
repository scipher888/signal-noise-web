import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e77-singularity-analogy', 'artifact': 'episode', 'type': 'comparison', 'story': 'Aaronson Thanksgiving advice', 'quote': 'this past week feels like the opening chapter of an AI singularity'}


def check(ctx):
    return ctx.require('framing', r'(?=.*(?:past|last|this) week)(?=.*(?:feels|felt) like)(?=.*(?:opening chapter|beginning|start) of (?:an? |the )?AI singularity)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
