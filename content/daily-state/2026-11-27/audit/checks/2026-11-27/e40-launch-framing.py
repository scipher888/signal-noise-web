import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e40-launch-framing', 'artifact': 'episode', 'type': 'attribution', 'story': 'Anthropic capability limits', 'quote': 'In that launch post, Anthropic framed its limits under safety and alignment'}


def check(ctx):
    return ctx.require('claude', r'(?:launch|Anthropic|November).*safety and alignment', note='Verify the launch post’s own framing, not a commenter’s view of alignment.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
