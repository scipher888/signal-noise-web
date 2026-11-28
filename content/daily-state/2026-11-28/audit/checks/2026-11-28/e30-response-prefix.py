import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e30-response-prefix', 'artifact': 'episode', 'type': 'attribution', 'story': 'Mir2k', 'quote': 'The new template quietly instructed the model to begin every response with a PowerShell line'}


def check(ctx):
    return ctx.require('gguf', r'In the Mir2k models, the template adds a system message telling the model to begin every answer with one PowerShell line')


if __name__ == '__main__':
    run_cli(CLAIM, check)
