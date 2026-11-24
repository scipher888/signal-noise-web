import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'tc01-citation', 'artifact': 'takeaways', 'type': 'citation', 'story': 'takeaway 1', 'quote': None}
URL = 'https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/'
ALLOWED = ['https://cset.georgetown.edu/article/judge-the-cyber-apocalypse-by-the-data-not-the-headlines/', 'https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification/', 'https://openai.com/index/a-thousand-fewer-paths-to-root/', 'https://openai.com/index/introducing-shirudo/', 'https://www.anthropic.com/research/working-with-ai', 'https://x.com/GoogleDeepMind/status/2124911073266413634', 'https://x.com/OpenAI/status/2124980590717911527', 'https://x.com/OpenAI/status/2125007927098699827', 'https://x.com/emollick/status/2125098309928812898', 'https://x.com/ramez/status/2125004190032552392']


def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))


if __name__ == '__main__':
    run_cli(CLAIM, check)
