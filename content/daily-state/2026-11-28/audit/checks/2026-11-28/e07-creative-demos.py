import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e07-creative-demos', 'artifact': 'episode', 'type': 'attribution', 'story': 'OpenAI demos', 'quote': 'demos of Astra building mechanical assemblies in CAD, racing games in the browser, and animations in Blender'}


def check(ctx):
    return ctx.require('gpt', r'individual parts and connections in CAD', r'modeled the individual components, created an animated assembly guide', r'Astra builds a playable futuristic racing game', r'interactive browser experience', r'Astra created the 3D model.*animated the results in Blender')


if __name__ == '__main__':
    run_cli(CLAIM, check)
