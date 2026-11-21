import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e41-narayanan-business-trap', 'artifact': 'episode', 'type': 'attribution', 'story': 'Arvind Narayanan warning', 'quote': "Princeton's Arvind Narayanan, who warned today that racing on verifiable capabilities and efficiency is a business trap for frontier labs"}


def check(ctx):
    s1 = ctx.find('random_walker', r'racing to self-improve the verifiable subset of capabilities.*sustainable businesses')
    s2 = ctx.find('random_walker', r'Princeton computer scientist')
    if s1 and s2:
        if ctx.absent('random_walker', r'efficien'):
            return ctx.need('random_walker', s1, 'Narayanan warns on verifiable capabilities and sustainable businesses, but does not mention efficiency in this post')
        return ctx.ok('random_walker', s1)
    return ctx.need('random_walker', s1 or s2, 'Check Narayanan attribution')


if __name__ == '__main__':
    run_cli(CLAIM, check)
