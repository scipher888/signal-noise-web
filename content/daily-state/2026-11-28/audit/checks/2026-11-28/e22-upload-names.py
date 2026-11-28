import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e22-upload-names', 'artifact': 'episode', 'type': 'attribution', 'story': 'Mir2k', 'quote': 'First, the attacker uploaded uncensored GGUF builds of Qwen 3.5 and Inkling 2 Mini'}


def check(ctx):
    return ctx.require('gguf', r'Mir2k, uploaded two uncensored GGUF models', r'On 22 November, Huihui-Qwen3\.5-9B-abliterated was uploaded', r'On 24 November, Inkling-2-Mini-Uncensored followed')


if __name__ == '__main__':
    run_cli(CLAIM, check)
