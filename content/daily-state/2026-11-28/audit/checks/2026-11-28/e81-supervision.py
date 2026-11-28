import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e81-supervision', 'artifact': 'episode', 'type': 'opinion', 'story': 'Model supervision', 'quote': 'Inspecting and supervising what steers the model after you hit enter is the job now'}


def check(ctx):
    return ctx.need('gguf', ctx.find('gguf', r'People who run community models locally should treat any command a model suggests as untrusted'), 'Editorial recommendation extending beyond the local-model advice.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
