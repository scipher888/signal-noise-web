import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't18-core-authorship', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Messages API migration', 'quote': 'Claude wrote the core request path'}


def check(ctx):
    return ctx.support_or_contradict('anthropic', r'Claude wrote the (?:API.s )?core request path', r'Claude wrote a first version of the API.s core request path', 'Authorship is explicitly scoped to a first version.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
