import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e62-shared-assumption', 'artifact': 'episode', 'type': 'comparison', 'story': 'AI acceleration boundary', 'quote': 'Measuring AI-accelerated research in a loss curve and quarantining it behind a classifier both assume a sharp border between routine machine learning and frontier self-improvement.'}


def check(ctx):
    return ctx.need('claude', ctx.find('claude', r'where the limits actually stop'), 'Conceptual analogy, not a shared assumption established by the sources.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
