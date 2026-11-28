import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'tc01-citation', 'artifact': 'takeaways', 'type': 'citation', 'story': 'takeaway 1', 'quote': None}
URL = 'https://malspark.com/blog/malicious-gguf-models-hugging-face/'
ALLOWED = ['https://every.to/live/openai-astra-sol', 'https://github.com/Root0ne/gguf-radar', 'https://github.com/unslothai/unsloth', 'https://malspark.com/blog/malicious-gguf-models-hugging-face/', 'https://openai.com/index/introducing-gpt-6-2-astra-sol/', 'https://unsloth.ai/docs/basics/mcp/mcp-engines', 'https://x.com/ItsmeAjayKV/status/2126546800291266717', 'https://x.com/TheZvi/status/2126309705131651174', 'https://x.com/UnslothAI/status/2126322382239649959']


def check(ctx):
    if URL and URL in ALLOWED:
        return ctx.ok(None, None, 'Takeaway 1 cites ' + URL + ', which is listed in the episode sources.json.')
    return ctx.fail(None, None, 'Takeaway 1 cites %s, which is not in the episode sources.json.' % (URL or 'no URL'))


if __name__ == '__main__':
    run_cli(CLAIM, check)
