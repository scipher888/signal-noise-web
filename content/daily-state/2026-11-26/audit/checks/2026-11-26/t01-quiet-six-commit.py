import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't01-quiet-six-commit', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Cogentic papers', 'quote': 'Google Research quietly committed six new math papers to GitHub'}


def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*Google Research)(?=.*(?:quietly|without announcement))(?=.*six (?:new )?(?:math|Cogentic) papers)(?=.*GitHub)', r'Google Research posts six Cogentic papers', 'The posting and count are reported; quiet publication is not.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
