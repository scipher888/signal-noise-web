import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e23-qualifier-adjusting-ambiguous-tool', 'artifact': 'episode', 'type': 'qualifier', 'story': 'AI task-horizon analysis', 'quote': 'even after adjusting for ambiguous requests and tool errors'}


def check(ctx):
    return ctx.require('naam', r'ambiguous.*errors in the tools')


if __name__ == '__main__':
    run_cli(CLAIM, check)
