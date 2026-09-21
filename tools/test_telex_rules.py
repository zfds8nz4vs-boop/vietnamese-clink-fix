import runpy,sys,unittest
from pathlib import Path
class TelexRulesTest(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  old=sys.argv
  try:
   sys.argv=["build-telex-cime.py","vi","source/vi.txt"]
   ns=runpy.run_path(str(Path(__file__).with_name("build-telex-cime.py")),run_name="__test__")
  finally: sys.argv=old
  cls.telex=staticmethod(ns["syllable"]); cls.aliases=staticmethod(ns["aliases"]); cls.rows=ns["rows"]
 def test_canonical(self):
  cases={"áo":"aos","áu":"aus","tiếng":"tieengs","Việt":"Vieetj","đường":"dduowngf","người":"nguwowif"}
  for w,r in cases.items(): self.assertEqual(self.telex(w),r)
 def test_modern_and_old_aliases(self):
  for w,r in {"hòa":"hoaf","hoà":"hoaf","khỏe":"khoer","huỷ":"huyr","quý":"quys","của":"cuar","mía":"misa","ngoáy":"ngoasy","thoải":"thoair","quyết":"quyeets"}.items(): self.assertIn(r,self.aliases(w))
  self.assertIn("hofa",self.aliases("hòa")); self.assertIn("hury",self.aliases("hủy"))
 def test_positions(self):
  for w,r in {"bài":"bafi","bảy":"bayr","của":"cuar","chiều":"chieefu","chuối":"chuoosi","mười":"muwowfi","nước":"nuwowsc","biển":"bieern","quyền":"quyeefn"}.items(): self.assertIn(r,self.aliases(w))
 def test_literal(self):
  for r in ("aaa","aaaa","eeee","oooooooo","ss","ff","rr","xx","jj","zz"): self.assertIn(r,self.rows[r])
  self.assertIn("ưw",self.rows["uww"]); self.assertIn("ơw",self.rows["oww"]); self.assertIn("ăw",self.rows["aww"])
if __name__=="__main__": unittest.main()
