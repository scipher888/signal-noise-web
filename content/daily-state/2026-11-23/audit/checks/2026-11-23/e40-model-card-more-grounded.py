import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e40-model-card-more-grounded', 'artifact': 'episode', 'type': 'comparison', 'story': 'Ant Group LingSante', 'quote': 'the model card tells a more grounded story than the launch post'}


def check(ctx):
    return ctx.need(None, None, 'Editorial comparison of tone between model card and launch post')


if __name__ == '__main__':
    run_cli(CLAIM, check)
