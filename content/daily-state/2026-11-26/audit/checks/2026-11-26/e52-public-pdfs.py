import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e52-public-pdfs', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Google formalizations', 'quote': 'Outside mathematicians can read the PDFs today'}


def check(ctx):
    q = ctx.find('framing', r'Company-posted preprints in a public repository')
    if not q: return ctx.need('framing', None, 'Need public availability.')
    p = ctx.find('google', r'\[This paper\]\(paper\.pdf\)')
    return ctx.need('google', p, 'One linked PDF; public preprints do not establish that all the PDFs are readable today.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
