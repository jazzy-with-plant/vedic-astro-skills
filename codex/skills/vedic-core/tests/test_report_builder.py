import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "report_builder.py"
SPEC = importlib.util.spec_from_file_location("report_builder", SCRIPT)
REPORT_BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REPORT_BUILDER)


class ReportBuilderTests(unittest.TestCase):
    def test_root_and_parts_are_merged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "parts").mkdir()
            (root / "p1_overview.md").write_text("# 总览", encoding="utf-8")
            (root / "parts" / "qa_one.md").write_text("# 问答一", encoding="utf-8")
            (root / "parts" / "qa_two.md").write_text("# 问答二", encoding="utf-8")

            found = REPORT_BUILDER.find_files_multi([str(root), str(root / "parts")])

            self.assertIn("identity", found)
            self.assertIn("qa", found)
            self.assertIn("问答一", found["qa"][5])
            self.assertIn("问答二", found["qa"][5])

    def test_beginner_mode_groups_and_collapses_detail(self):
        found = {
            "summary": (1, "summary", "", "核心结论", "Summary", "# 一句话总览\n结论"),
            "career1": (60, "G6", "", "事业", "Career", "# 事业细节\n内容"),
            "love1": (80, "G7", "", "感情", "Love", "# 感情细节\n内容"),
            "planets_a": (15, "G1", "A", "行星", "Planets", "# 技术内容\n数据"),
        }

        sections = REPORT_BUILDER.build_beginner_sections(found, "cn")
        titles = [title for title, _ in sections]
        joined = "".join(body for _, body in sections)

        self.assertEqual(titles, ["先看这页：核心结论", "事业与工作", "感情与关系", "技术依据与完整审计"])
        self.assertEqual(joined.count('<details class="reader-details">'), 3)
        self.assertIn("一句话总览", joined)


if __name__ == "__main__":
    unittest.main()
