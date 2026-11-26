import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e67-ai-machinery-limits', 'artifact': 'episode', 'type': 'attribution', 'story': 'Dual-use mathematics', 'quote': 'When AI builds powerful new mathematical machinery, it does not only prove reassuring limits on what computers cannot do'}


def check(ctx):
    return ctx.need('framing', ctx.find('framing', r'claiming results on factoring, the log-rank conjecture'), 'A list of claimed results cannot establish the general mechanism or that these are impossibility results.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
