import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't14-research-not-clinical-diagnosis', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Ant Group LingSante-3.1-flash', 'quote': 'for research, not clinical diagnosis'}


def check(ctx):
    return ctx.require('lingsante', r'intended for research and evaluation', r'must not be used as an independent basis for diagnosis')


if __name__ == '__main__':
    run_cli(CLAIM, check)
