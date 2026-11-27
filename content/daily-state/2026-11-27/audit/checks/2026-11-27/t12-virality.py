import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't12-virality', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Claude refusal behavior', 'quote': 'Viral claims'}


def check(ctx):
    return ctx.require('claude', r'The charge went viral', r'The post has passed 1\.2 million views')


if __name__ == '__main__':
    run_cli(CLAIM, check)
