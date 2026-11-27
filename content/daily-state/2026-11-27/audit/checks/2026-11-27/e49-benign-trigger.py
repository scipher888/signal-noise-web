import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e49-benign-trigger', 'artifact': 'episode', 'type': 'attribution', 'story': 'API refusal and fallback behavior', 'quote': 'Anthropic acknowledges that benign machine-learning work can trigger it'}


def check(ctx):
    return ctx.require('framing', r'(?:Anthropic|Company documentation).*benign (?:ML|machine.learning).*?(?:trigger|refus)', note='Need company documentation about false positives, not anecdotes about refusals.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
