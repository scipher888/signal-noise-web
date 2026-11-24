import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e17-gpt6-cyber-patches', 'artifact': 'episode', 'type': 'attribution', 'story': 'Linux Cybersecurity', 'quote': 'its GPT-6 Cyber pipeline validated and generated patches'}


def check(ctx):
    return ctx.require('openai2', r'GPT-6 Cyber helped us validate.*generate patches')


if __name__ == '__main__':
    run_cli(CLAIM, check)
