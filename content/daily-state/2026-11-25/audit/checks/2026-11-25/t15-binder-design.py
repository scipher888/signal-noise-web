import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't15-binder-design', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'GPT-6 protein binders', 'quote': 'its GPT-6 models used reasoning and code to design protein binders'}


def check(ctx):
    return ctx.require('openai', r'Our GPT.6 family of models can design new protein shapes.*using only reasoning and code', r'GPT.6\.2 designed shapes for small proteins intended to attach to chosen targets')


if __name__ == '__main__':
    run_cli(CLAIM, check)
