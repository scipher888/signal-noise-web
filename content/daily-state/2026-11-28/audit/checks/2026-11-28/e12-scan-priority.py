import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e12-scan-priority', 'artifact': 'episode', 'type': 'comparison', 'story': 'GGUF scan', 'quote': 'the first scan of all 3.27 million public repositories on Hugging Face'}


def check(ctx):
    return ctx.support_or_contradict('gguf', r'first scan of all (?:3\.27 million|3273389) public Hugging Face repositories', r'What this post adds is the method seen in real attacks.*no earlier public report', 'The novelty statement concerns a technique observed in the wild, not priority of a platform-wide census.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
