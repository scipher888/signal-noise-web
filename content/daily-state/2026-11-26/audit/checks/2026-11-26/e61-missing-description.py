import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e61-missing-description', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Shadow oracle', 'quote': 'a web search tool description was missing'}


def check(ctx):
    return ctx.require('anthropic', r'production API retrieved the web search tool.s description from an internal service', r'the tool description was missing from the prompts')


if __name__ == '__main__':
    run_cli(CLAIM, check)
