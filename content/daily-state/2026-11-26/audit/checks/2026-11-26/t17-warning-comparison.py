import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't17-warning-comparison', 'artifact': 'takeaways', 'type': 'comparison', 'story': 'RSA rumors', 'quote': "X posts claiming frontier labs secretly cracked RSA encryption overstated Scott Aaronson's warning"}


def check(ctx):
    q = ctx.find('framing', r'explicitly declines to vouch for the specifics')
    return ctx.support_or_contradict('andrewcurran_', r'(?:secretly|privately) (?:cracked|broke) RSA', r'This would crack RSA', 'Posts speculate beyond the warning but this one does not assert a completed crack. ' + (q or ''))


if __name__ == '__main__':
    run_cli(CLAIM, check)
