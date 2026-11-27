import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e42-cap-domains', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Anthropic capability limits', 'quote': 'including accelerator kernel optimization and language-model architecture'}


def check(ctx):
    return ctx.require('claude', r'cap covers two capabilities — optimizing accelerator kernels and improving large language model architectures')


if __name__ == '__main__':
    run_cli(CLAIM, check)
