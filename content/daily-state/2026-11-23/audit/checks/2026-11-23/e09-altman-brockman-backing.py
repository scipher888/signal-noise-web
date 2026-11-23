import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e09-altman-brockman-backing', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI Perplexity', 'quote': 'backed publicly by Sam Altman and Greg Brockman'}


def check(ctx):
    s1 = ctx.find('sama', r'most important thing OpenAI has published')
    s2 = ctx.find('gdb', r'foundation of industry-wide shared safety bars')
    if s1 and s2:
        return ctx.ok('sama', s1, 'Both Sam Altman and Greg Brockman publicly endorsed the post')
    return ctx.need('sama', s1 or s2, 'Could not confirm public backing from both Altman and Brockman')


if __name__ == '__main__':
    run_cli(CLAIM, check)
