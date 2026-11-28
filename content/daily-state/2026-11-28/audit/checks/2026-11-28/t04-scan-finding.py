import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't04-scan-finding', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'GGUF scan', 'quote': 'found five active malicious GGUF models'}


def check(ctx):
    return ctx.require('gguf', r'scan of all 3273389 public Hugging Face model repositories.*found 5 malicious GGUF models', r'Five repositories remained, all still online on 27 November')


if __name__ == '__main__':
    run_cli(CLAIM, check)
