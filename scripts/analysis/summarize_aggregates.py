"""Summarize already computed public aggregate values; no model or bootstrap."""
import argparse, csv, hashlib, json
from pathlib import Path
EXPECTED={"stage31_condition_results_corrected.csv":"d46ee44764b7611b7277dc83e6412b55d398a084b2a5fb55062c5b54dbdd8ca9", "stage30_four_group_metrics.csv":"d7c316bd043ddcca38dbd92e1c69e341a6a5ccf27a464742ac6ee07dbe4979d4"}
def read(path):
    if hashlib.sha256(path.read_bytes()).hexdigest()!=EXPECTED[path.name]: raise ValueError("Input SHA-256 mismatch: "+path.name)
    with path.open(encoding="utf-8-sig", newline="") as f: return list(csv.DictReader(f))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--input-dir",type=Path,required=True); ap.add_argument("--output-dir",type=Path,required=True); ap.add_argument("--interaction-json",type=Path,help="Optional public post-hoc interaction JSON"); a=ap.parse_args()
    conditions=read(a.input_dir/"stage31_condition_results_corrected.csv"); metrics=read(a.input_dir/"stage30_four_group_metrics.csv")
    if len(conditions)!=152: raise ValueError("Expected 152 condition-level records")
    keys={(r["dataset"],r["model"],r["probability_state"],r["metric"]):r for r in metrics}
    result=[]
    for d,m,_,metric in sorted(keys):
        if (d,m,"raw",metric) in keys and (d,m,"calibrated",metric) in keys and (d,m,metric) not in {(x["dataset"],x["model"],x["metric"]) for x in result}:
            raw=keys[d,m,"raw",metric]["value"]; cal=keys[d,m,"calibrated",metric]["value"]
            result.append(dict(dataset=d,model=m,metric=metric,raw=raw,calibrated=cal,calibrated_minus_raw=float(cal)-float(raw)))
    a.output_dir.mkdir(parents=True,exist_ok=True)
    with (a.output_dir/"aggregate_metric_changes.csv").open("w",encoding="utf8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=["dataset","model","metric","raw","calibrated","calibrated_minus_raw"]);writer.writeheader();writer.writerows(result)
    with (a.output_dir/"condition_accuracy.csv").open("w",encoding="utf8",newline="") as f:
        fields=["dataset","model","condition","family","accuracy"]
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");writer.writeheader();writer.writerows(r for r in conditions if r["probability_state"]=="raw")
    if a.interaction_json:
        raw_interaction=a.interaction_json.read_bytes()
        if hashlib.sha256(raw_interaction).hexdigest()!="d498bd6416e0ce66af8414388a1799c350f4719c83e293680d607f035304645b": raise ValueError("Interaction input SHA-256 mismatch")
        interaction=json.loads(raw_interaction)
        fields=["metric","estimand","b32_plugin_delta","l14_plugin_delta","plugin_difference_in_differences","bootstrap_interaction_mean","bootstrap_interaction_ci"]
        with (a.output_dir/"interaction_as_recorded.csv").open("w",encoding="utf8",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore");writer.writeheader();writer.writerows(interaction["results"])
        print("Interaction values exported as recorded; direction and estimand are not relabeled.")
    print("Wrote aggregate metric differences and 76 raw condition-accuracy rows; no new inference or uncertainty estimates.")
if __name__=="__main__": main()
