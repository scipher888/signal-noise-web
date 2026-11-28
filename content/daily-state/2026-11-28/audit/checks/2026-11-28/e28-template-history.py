import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e28-template-history', 'artifact': 'episode', 'type': 'attribution', 'story': 'Mir2k', 'quote': "Days later, on November 26th, Mir2k swapped out each model's hidden Jinja2 chat template twice in nine hours"}


def check(ctx):
    return ctx.require('gguf', r'chat template is a small Jinja2 program', r'Mir2k.*on 26 November rewrote both templates', r'morning of 26 November both templates were replaced', r'Nine hours later both were replaced again', r'template is changed two to four days later')


if __name__ == '__main__':
    run_cli(CLAIM, check)
