import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e13-scan-universe', 'artifact': 'episode', 'type': 'number', 'story': 'GGUF scan', 'quote': 'all 3.27 million public repositories on Hugging Face'}


def check(ctx):
    return ctx.support_or_contradict('gguf', r'all 3273389 public Hugging Face repositories', r'all 3273389 public Hugging Face model repositories', 'Correct rounded count, wrong universe: model repositories only.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
