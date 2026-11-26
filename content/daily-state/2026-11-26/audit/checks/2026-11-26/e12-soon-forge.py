import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e12-soon-forge', 'artifact': 'episode', 'type': 'qualifier', 'story': 'RSA rumors', 'quote': 'could soon forge software updates across the internet'}


def check(ctx):
    return ctx.support_or_contradict('kimmonismus', r'(?:soon|shortly).*fake software updates', r'Fake software updates could pass signature checks', 'Hypothetical effect; the post gives no timeline.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
