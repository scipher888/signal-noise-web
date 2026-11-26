import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'tc01-citation', 'artifact': 'takeaways', 'type': 'citation', 'story': 'takeaway 1', 'quote': None}
URL = 'https://github.com/google-research/google-research/commit/4a7bc8ab0bc770e71a259b7966c500496b99010a'
ALLOWED = ['https://github.com/google-research/google-research/commit/4a7bc8ab0bc770e71a259b7966c500496b99010a', 'https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/integer_factorization/README.md', 'https://raw.githubusercontent.com/google-research/google-research/master/cogentic_research_papers/logrank_conjecture/README.md', 'https://scottaaronson.blog/?p=10379', 'https://x.com/AndrewCurran_/status/2125596087520223658', 'https://x.com/kimmonismus/status/2125574747882704951', 'https://x.com/kimmonismus/status/2125602411540566221']


def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))


if __name__ == '__main__':
    run_cli(CLAIM, check)
