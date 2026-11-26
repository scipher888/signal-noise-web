import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e04-engineering-post', 'artifact': 'episode', 'type': 'attribution', 'story': 'Rust migration', 'quote': 'a methodical Anthropic engineering post about migrating its Messages API from Python to Rust'}


def check(ctx):
    return ctx.require('anthropicai', r'@AnthropicAI: We recently migrated our Messages API from Python to Rust', r'On our engineering blog, we share how we used the existing service to verify the new one')


if __name__ == '__main__':
    run_cli(CLAIM, check)
