import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e10-labs-agents', 'artifact': 'episode', 'type': 'attribution', 'story': 'Society', 'quote': 'thirty-five human labs, including Stanford, MIT, and ETH Zurich, deployed 936 autonomous agents onto a shared preprint server'}


def check(ctx):
    return ctx.require('society', r'936 autonomous agents across 35 human-operated laboratories .*shared preprint server', r'35 labs \(across Stanford, MIT, ETH Zurich')


if __name__ == '__main__':
    run_cli(CLAIM, check)
