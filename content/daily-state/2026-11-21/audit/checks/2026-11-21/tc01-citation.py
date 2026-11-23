import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'tc01-citation', 'artifact': 'takeaways', 'type': 'citation', 'story': 'takeaway 1', 'quote': None}
URL = 'https://alpo.ge/remark.pdf'
ALLOWED = ['https://alpo.ge/remark.pdf', 'https://thinkingmachines.ai/news/inkling-2-mini/', 'https://www.rameznaam.com/p/the-most-important-charts-in-ai-are', 'https://x.com/0xSero/status/2123883583740006752', 'https://x.com/AndrewCurran_/status/2123819916768039149', 'https://x.com/ArtificialAnlys/status/2123865423364161861', 'https://x.com/emollick/status/2123800664845500602', 'https://x.com/emollick/status/2123972584400204199', 'https://x.com/ramez/status/2123934198868382184', 'https://x.com/ramez/status/2123944723492782408', 'https://x.com/random_walker/status/2123869355431661866', 'https://x.com/soumithchintala/status/2123878334895436115']


def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))


if __name__ == '__main__':
    run_cli(CLAIM, check)
