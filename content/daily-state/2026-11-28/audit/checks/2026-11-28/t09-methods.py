import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't09-methods', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'GGUF scan', 'quote': 'using hidden trailing payloads or poisoned chat templates'}


def check(ctx):
    return ctx.require('gguf', r'Mir2k, hides a Windows remote access trojan at the end of GGUF files and later arms the chat template', r'In the timdedid models, a trigger phrase.*makes the template insert a fake')


if __name__ == '__main__':
    run_cli(CLAIM, check)
