import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e08-reality-check', 'artifact': 'episode', 'type': 'opinion', 'story': 'Two headlines', 'quote': "Anthropic's post is the sharpest reality check against assuming an overnight math singularity translates straight into messy real-world systems"}


def check(ctx):
    return ctx.need('anthropic', ctx.find('anthropic', r'generating the work is easier than verifying it'), 'Sharpest is an editorial ranking.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
