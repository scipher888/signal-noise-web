import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e63-every-population', 'artifact': 'episode', 'type': 'attribution', 'story': 'Astra feedback', 'quote': "Every's thirty-person frontier team said no one on staff loved Astra or switched back to it"}


def check(ctx):
    q = ctx.find('thezvi', r'30-person team at Every, including our Frontier team')
    if q: return ctx.fail('thezvi', q, 'The subgroup is not 30 people. Switching was also qualified: ' + str(ctx.find('thezvi', r'No one on our team who tried it switched back to it')))
    return ctx.require('thezvi', r'30-person Frontier team', r'No one on our team loved Astra', r'No one on (?:our )?staff switched back')


if __name__ == '__main__':
    run_cli(CLAIM, check)
