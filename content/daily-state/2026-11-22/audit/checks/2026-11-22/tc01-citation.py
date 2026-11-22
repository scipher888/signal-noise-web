import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'tc01-citation', 'artifact': 'takeaways', 'type': 'citation', 'story': 'takeaway 1', 'quote': None}
URL = 'https://metr.org/blog/2026-11-20-q4-2026-capability-update'
ALLOWED = ['https://leanprover-community.github.io/blog/posts/riemann-hypothesis/', 'https://metr.org/blog/2026-11-20-q4-2026-capability-update', 'https://natolambert.com/slides/2026/cornell-post-training/talk', 'https://x.com/DKThomp/status/2124156773560902109', 'https://x.com/emollick/status/2124173181065806006', 'https://x.com/natolambert/status/2124152733145923892', 'https://x.com/ramez/status/2124216462374216181', 'https://x.com/ramez/status/2124298418403311694']


def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))


if __name__ == '__main__':
    run_cli(CLAIM, check)
