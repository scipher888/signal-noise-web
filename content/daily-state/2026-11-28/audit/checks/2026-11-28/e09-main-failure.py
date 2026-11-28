import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e09-main-failure', 'artifact': 'episode', 'type': 'opinion', 'story': 'App control risks', 'quote': "turns the hidden layer between a human prompt and a model's actions into the main point of failure, both from outside attackers and from the models themselves"}


def check(ctx):
    return ctx.need('gguf', ctx.find('gguf', r'template quietly adds instructions the user never sees'), 'A demonstrated failure mode does not rank it against other causes.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
