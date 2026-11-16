"""Smoke tests using verified aggregate inputs supplied by RELEASE_DATA_DIR."""
import importlib.util, os, subprocess, sys, tempfile, unittest, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
NAMES=["fig4_calibration_readable","fig5_accuracy_readable","fig6_selective_horizontal","fig7_nll_readable","fig8_brier_readable","fig10_auroc_readable"]
class ReleaseSmoke(unittest.TestCase):
 def test_imports(self):
  for path in [ROOT/"scripts/figures/plot_figures.py",ROOT/"scripts/analysis/summarize_aggregates.py",ROOT/"config/plotting_style/style.py"]:
   spec=importlib.util.spec_from_file_location(path.stem,path); mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 def test_aggregate_inputs_and_outputs(self):
  data=os.environ.get("RELEASE_DATA_DIR")
  if not data: self.skipTest("Set RELEASE_DATA_DIR to the three verified aggregate CSV files")
  with tempfile.TemporaryDirectory() as tmp:
   for script in ["figures/plot_figures.py","analysis/summarize_aggregates.py"]:
    subprocess.run([sys.executable,str(ROOT/"scripts"/script),"--input-dir",data,"--output-dir",tmp],check=True)
   for name in NAMES:
    with Image.open(Path(tmp)/(name+".png")) as image: image.verify()
    self.assertTrue(ET.parse(Path(tmp)/(name+".svg")).getroot().tag.endswith("svg"))
   self.assertTrue((Path(tmp)/"aggregate_metric_changes.csv").is_file())
   self.assertTrue((Path(tmp)/"condition_accuracy.csv").is_file())
   interaction=Path(data)/"ivc_oxford_calibration_interaction_posthoc.json"
   if interaction.exists():
    subprocess.run([sys.executable,str(ROOT/"scripts/analysis/summarize_aggregates.py"),"--input-dir",data,"--output-dir",tmp,"--interaction-json",str(interaction)],check=True)
    self.assertTrue((Path(tmp)/"interaction_as_recorded.csv").is_file())
 def test_tampered_aggregate_rejected(self):
  data=os.environ.get("RELEASE_DATA_DIR")
  if not data: self.skipTest("Set RELEASE_DATA_DIR for hash validation")
  with tempfile.TemporaryDirectory() as tmp:
   source=Path(data)/"stage30_four_group_metrics.csv"
   (Path(tmp)/source.name).write_bytes(source.read_bytes()+b"tampered")
   r=subprocess.run([sys.executable,str(ROOT/"scripts/figures/plot_figures.py"),"--input-dir",tmp,"--output-dir",tmp,"--figures","4"],capture_output=True,text=True)
   self.assertNotEqual(r.returncode,0); self.assertIn("SHA-256",r.stderr)
 def test_unavailable_figures_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   for fig in ["8","S1"]:
    r=subprocess.run([sys.executable,str(ROOT/"scripts/figures/plot_figures.py"),"--input-dir",tmp,"--output-dir",tmp,"--figures",fig],capture_output=True,text=True)
    self.assertNotEqual(r.returncode,0); self.assertIn("invalid choice",r.stderr)
if __name__=="__main__": unittest.main()
