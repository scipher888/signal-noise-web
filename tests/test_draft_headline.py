"""draft_headline.py asks or-call for Neon (medium), then Astra (medium). No network."""

import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("draft_headline", REPO / "tools" / "draft_headline.py")
draft_headline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(draft_headline)

FAKE = """#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
out = args[args.index("--out") + 1]
open(out, "w").write("Verification Becomes the Bottleneck for AI Work\\n")
json.dump({"argv": args, "stdin": sys.stdin.read(),
           "terra": os.environ.get("OR_OFFLOAD_MODEL_TERRA"),
           "sol": os.environ.get("OR_OFFLOAD_MODEL_SOL")},
          open(os.environ["FAKE_LOG"], "w"))
print(json.dumps({"ok": True, "model": os.environ.get("OR_OFFLOAD_MODEL_TERRA")}))
"""


class DraftHeadlineModelTests(unittest.TestCase):
    def test_neon_then_astra_at_medium_and_prompt_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            fake = tmp / "or-call"
            fake.write_text(FAKE)
            fake.chmod(0o755)
            script = tmp / "script.txt"
            script.write_text("An episode script.\n")
            log = tmp / "log.json"
            os.environ["FAKE_LOG"] = str(log)
            old = draft_headline.OR_CALL
            draft_headline.OR_CALL = str(fake)
            try:
                with redirect_stdout(io.StringIO()) as out:
                    code = draft_headline.main([
                        "--date", "2026-11-24", "--script", str(script), "--out", str(tmp / "h.txt"),
                    ])
            finally:
                draft_headline.OR_CALL = old
                os.environ.pop("FAKE_LOG", None)
            self.assertEqual(code, 0)
            seen = json.loads(log.read_text())
            argv = seen["argv"]
            self.assertEqual(argv[argv.index("--model") + 1], "terra")
            self.assertEqual(seen["terra"], "google/gemini-4-neon")
            self.assertEqual(seen["sol"], "openai/gpt-6.2-astra")
            self.assertEqual(seen["stdin"], draft_headline.PROMPT)
            self.assertEqual(draft_headline.PROMPT, (
                "Write a 4-10 word headline for this Daily State of AI episode that "
                "captures its central insight. Plain text, no quotes."))
            self.assertEqual(json.loads(out.getvalue())["headline"],
                             "Verification Becomes the Bottleneck for AI Work")
            self.assertNotIn("OR_OFFLOAD_MODEL_TERRA", os.environ)

    def test_reuses_headline_txt_beside_the_script_without_or_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            script = tmp / "script.txt"
            script.write_text("An episode script.\n")
            headline = "AI Is Built for Discovery, Not Everyday Reliability"
            (tmp / "headline.txt").write_text(headline + "\n")
            fake = tmp / "or-call"
            fake.write_text("#!/bin/sh\nexit 99\n")
            fake.chmod(0o755)
            old = draft_headline.OR_CALL
            draft_headline.OR_CALL = str(fake)
            try:
                with redirect_stdout(io.StringIO()) as out:
                    code = draft_headline.main([
                        "--date", "2026-11-26", "--script", str(script),
                        "--out", str(tmp / "h.txt"),
                    ])
            finally:
                draft_headline.OR_CALL = old
            self.assertEqual(code, 0)
            self.assertEqual((tmp / "h.txt").read_text(), headline + "\n")
            payload = json.loads(out.getvalue())
            self.assertEqual(payload["headline"], headline)
            self.assertTrue(payload["reused"])
            self.assertEqual(payload["source"], str(tmp / "headline.txt"))

    def test_invalid_headline_txt_falls_through_to_or_call(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            fake = tmp / "or-call"
            fake.write_text(FAKE)
            fake.chmod(0o755)
            script = tmp / "script.txt"
            script.write_text("An episode script.\n")
            (tmp / "headline.txt").write_text("too\nmany\nlines\n")
            log = tmp / "log.json"
            os.environ["FAKE_LOG"] = str(log)
            old = draft_headline.OR_CALL
            draft_headline.OR_CALL = str(fake)
            try:
                with redirect_stdout(io.StringIO()) as out:
                    code = draft_headline.main([
                        "--date", "2026-11-26", "--script", str(script),
                        "--out", str(tmp / "h.txt"),
                    ])
            finally:
                draft_headline.OR_CALL = old
                os.environ.pop("FAKE_LOG", None)
            self.assertEqual(code, 0)
            self.assertTrue(log.exists())
            self.assertEqual(json.loads(out.getvalue())["headline"],
                             "Verification Becomes the Bottleneck for AI Work")



if __name__ == "__main__":
    unittest.main()
