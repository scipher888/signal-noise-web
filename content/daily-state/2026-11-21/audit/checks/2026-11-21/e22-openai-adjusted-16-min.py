import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e22-openai-adjusted-16-min', 'artifact': 'episode', 'type': 'number', 'story': 'AI task-horizon analysis', 'quote': 'Inside OpenAI, even after adjusting for ambiguous requests and tool errors, it is sixteen minutes.'}


def check(ctx):
    return ctx.require('naam', r'adjusted 16 minutes at OpenAI', r'ambiguous.*errors in the tools')


if __name__ == '__main__':
    run_cli(CLAIM, check)
