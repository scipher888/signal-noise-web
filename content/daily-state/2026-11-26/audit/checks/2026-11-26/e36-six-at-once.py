import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e36-six-at-once', 'artifact': 'episode', 'type': 'number', 'story': 'Google papers', 'quote': 'six more at once'}


def check(ctx):
    return ctx.support_or_contradict('framing', r'six (?:more|additional) .*?(?:at once|together|single commit)', r'Google Research posts six Cogentic papers', 'The count is given, not the increment and timing.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
