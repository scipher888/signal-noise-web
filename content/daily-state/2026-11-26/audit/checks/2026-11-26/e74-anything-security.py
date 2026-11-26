import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e74-anything-security', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Disclosure divide', 'quote': 'Anything touching live security stays behind closed doors'}


def check(ctx):
    return ctx.support_or_contradict('framing', r'(?:anything|all results) (?:touching|affecting) live security .*private', r'No lab has published or confirmed such a result', 'Specific nonconfirmation is not a universal disclosure rule.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
