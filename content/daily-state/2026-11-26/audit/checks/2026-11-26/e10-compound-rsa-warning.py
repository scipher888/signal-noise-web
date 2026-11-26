import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e10-compound-rsa-warning', 'artifact': 'episode', 'type': 'attribution', 'story': 'RSA rumors', 'quote': 'Viral posts with thousands of likes were warning that frontier labs had secretly cracked RSA encryption and could soon forge software updates across the internet'}


def check(ctx):
    q = ctx.find('kimmonismus', r'If an algorithm like this actually works on real key sizes')
    return ctx.fail('kimmonismus', q, 'Conditional consequences, not a completed secret break or a near-term forecast; no original-post like count.') if q else ctx.need(None, None, 'Need the attributed warning and metrics.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
