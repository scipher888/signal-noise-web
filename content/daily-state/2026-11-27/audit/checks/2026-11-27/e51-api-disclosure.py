import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e51-api-disclosure', 'artifact': 'episode', 'type': 'qualifier', 'story': 'API refusal and fallback behavior', 'quote': 'refusals and fallbacks are technically disclosed in the API'}


def check(ctx):
    return ctx.require('framing', r'(?:API|Claude Platform docs).*refusal.*fallback.*(?:notice|block|disclos|signal)', note='Transparent fallback alone does not verify API signaling for both.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
