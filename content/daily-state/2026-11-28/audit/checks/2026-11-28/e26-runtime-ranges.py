import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e26-runtime-ranges', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Mir2k', 'quote': 'Inference runtimes such as llama.cpp and LM Studio read only declared tensor byte ranges and ignore trailing data'}


def check(ctx):
    return ctx.require('gguf', r'llama\.cpp and LM Studio read exactly the byte ranges the header points to and ignore everything else')


if __name__ == '__main__':
    run_cli(CLAIM, check)
