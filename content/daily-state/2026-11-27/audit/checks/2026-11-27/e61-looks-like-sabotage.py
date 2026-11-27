import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e61-looks-like-sabotage', 'artifact': 'episode', 'type': 'opinion', 'story': 'Claude sabotage allegations', 'quote': 'any misfired classifier or stubborn bug immediately looks like sabotage'}


def check(ctx):
    return ctx.need('capital_vmv', ctx.find('capital_vmv', r'any glitch, hallucination, or model error'), 'Commentary about perceived intent.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
