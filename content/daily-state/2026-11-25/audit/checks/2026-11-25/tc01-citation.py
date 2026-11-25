import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'tc01-citation', 'artifact': 'takeaways', 'type': 'citation', 'story': 'takeaway 1', 'quote': None}
URL = 'https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard'
ALLOWED = ['https://generativehistory.substack.com/p/gpt-62-astra-solves-a-historical', 'https://openai.com/index/gpt-6-models-demonstrate-intrinsic-protein-design-capabilities/', 'https://www.kaggle.com/benchmarks/deepmind/hfe/leaderboard', 'https://x.com/OpenAI/status/2125334383490105601', 'https://x.com/emollick/status/2125245031842042301', 'https://x.com/gdb/status/2125341356503748716', 'https://x.com/kaggle/status/2125313430303244739']


def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))


if __name__ == '__main__':
    run_cli(CLAIM, check)
