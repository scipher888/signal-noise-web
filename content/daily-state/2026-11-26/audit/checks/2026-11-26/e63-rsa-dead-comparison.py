import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e63-rsa-dead-comparison', 'artifact': 'episode', 'type': 'comparison', 'story': 'RSA rumors', 'quote': 'turning a calibrated warning into viral claims that RSA was dead'}


def check(ctx):
    return ctx.support_or_contradict('andrewcurran_', r'RSA (?:is|was) dead', r'This would crack RSA', 'Conditional consequence, not a declaration that RSA was dead; virality also unquantified.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
