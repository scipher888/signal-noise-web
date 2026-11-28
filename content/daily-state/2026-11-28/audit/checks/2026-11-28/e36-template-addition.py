import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e36-template-addition', 'artifact': 'episode', 'type': 'qualifier', 'story': 'timdedid', 'quote': 'kept the official chat template intact except for one hidden rule'}


def check(ctx):
    return ctx.require('gguf', r'official Qwen3 template with one addition near the end', r'text never appears in the chat window')


if __name__ == '__main__':
    run_cli(CLAIM, check)
