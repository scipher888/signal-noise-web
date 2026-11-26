import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e62-local-copy', 'artifact': 'episode', 'type': 'attribution', 'story': 'Shadow oracle', 'quote': 'the agent hardcoded the text locally instead of calling the internal service'}


def check(ctx):
    return ctx.require('anthropic', r'web search tool.s description from an internal service', r'Rust API didn.t call this service yet', r'An agent proposed a shortcut to copy the text into files that would be readable by Rust', r'The prompts then matched, and the fix passed the local verifier')


if __name__ == '__main__':
    run_cli(CLAIM, check)
