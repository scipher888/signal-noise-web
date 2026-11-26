import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't16-secretly', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'RSA rumors', 'quote': 'secretly'}


def check(ctx):
    return ctx.support_or_contradict('kimmonismus', r'(?:secretly|in secret) (?:broke|cracked) RSA', r'If this rumors are true, it would explain why OpenAI and Anthropic are holding back their latest models', 'Speculation about model withholding does not establish a secret break.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
