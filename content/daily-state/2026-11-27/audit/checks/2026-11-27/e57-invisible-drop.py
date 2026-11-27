import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e57-invisible-drop', 'artifact': 'episode', 'type': 'opinion', 'story': 'API refusal and fallback behavior', 'quote': 'Inside an uninstrumented harness, a sudden capability drop can easily feel invisible.'}


def check(ctx):
    return ctx.need('claude', ctx.find('claude', r'Researchers who build agents and model harnesses'), 'Inference about the user experience, not a documented test.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
