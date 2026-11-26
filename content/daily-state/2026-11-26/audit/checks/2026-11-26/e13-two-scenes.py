import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e13-two-scenes', 'artifact': 'episode', 'type': 'comparison', 'story': 'Dual-use mathematics', 'quote': 'Those two scenes look like separate worlds: quiet math commits on GitHub, and a cybersecurity scare on social media'}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'Company-posted preprints in a public repository'), 'The contrast and characterization as quiet are editorial.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
