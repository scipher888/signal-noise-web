import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e71-safe-theorem-policy', 'artifact': 'episode', 'type': 'attribution', 'story': 'Disclosure divide', 'quote': 'Labs quietly commit safe theorems to GitHub at dinner-table speed, with zero fanfare'}


def check(ctx):
    return ctx.support_or_contradict('framing', r'(?=.*labs)(?=.*safe theorems)(?=.*GitHub)(?=.*(?:during dinner|dinner.table speed))(?=.*(?:without announcement|zero fanfare))', r'Company-posted preprints in a public repository', 'One repository does not establish a multi-lab safety filter, cadence or publicity policy.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
