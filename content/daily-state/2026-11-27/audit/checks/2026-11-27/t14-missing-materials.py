import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't14-missing-materials', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Claude refusal behavior', 'quote': 'shared no prompts, code, or logs'}


def check(ctx):
    q = ctx.find('claude', r'His post and the Reddit thread contain no transcripts, prompts, or logs')
    return ctx.need('claude', q, 'This covers particular posts and does not verify the absence of shared code, prompts and logs for the whole set.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
