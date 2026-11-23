import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'tc01-citation', 'artifact': 'takeaways', 'type': 'citation', 'story': 'takeaway 1', 'quote': None}
URL = 'https://openai.com/index/perplexity-and-intelligence'
ALLOWED = ['https://huggingface.co/inclusionAI/LingSante-3.1-flash', 'https://openai.com/index/perplexity-and-intelligence', 'https://x.com/AntLingAGI/status/2124523916819648945', 'https://x.com/deredleritt3r/status/2124568402031435962', 'https://x.com/gdb/status/2124582684840399311', 'https://x.com/sama/status/2124551594691932405', 'https://x.com/swyx/status/2124583459356373052']


def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))


if __name__ == '__main__':
    run_cli(CLAIM, check)
