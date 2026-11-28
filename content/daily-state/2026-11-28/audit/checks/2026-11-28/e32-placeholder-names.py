import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e32-placeholder-names', 'artifact': 'episode', 'type': 'attribution', 'story': 'Mir2k', 'quote': 'Mir2k also pre-created twelve empty placeholder repositories named after anticipated releases like Qwen4 and Llama 4 Scout'}


def check(ctx):
    return ctx.require('gguf', r'Mir2k is a new Hugging Face account', r'On 22 November it created 14 repositories', r'Twelve of them are empty placeholders named after expected releases such as Qwen4-27B.*Llama-4-Scout')


if __name__ == '__main__':
    run_cli(CLAIM, check)
