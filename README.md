# Zero-shot CLIP reliability: reproduction code

The project-authored code is licensed under the MIT License, copyright 2026 Li Ruolei and Ru Yaohui. See `LICENSE` and the licensing section below.

## Scope and data

The frozen manuscript studies source-paired geometric evaluation. This package reproduces six quantitative figures from [Mendeley Data Version 1](https://data.mendeley.com/datasets/m7jtfvtwfv/1), DOI 10.17632/m7jtfvtwfv.1. The aggregate dataset is separately licensed CC BY 4.0; it is not included here. The package does not run CLIP inference, fit temperatures, recompute source-cluster bootstrap, or include model weights, original benchmark images, labels, or source-level predictions.

Figure 8 and Supplementary Figure S1 require an additional author-controlled aggregate input not included in the public Mendeley Version 1 dataset. The plotting entry point supports only the six figures listed below.

| Manuscript figure | Public input | Plot selection | Frozen asset |
|---|---|---|---|
| 4 | Four-group metrics CSV | `--figures 4` | `fig4_calibration_readable.png` |
| 5 | Corrected condition CSV | `--figures 5` | `fig5_accuracy_readable.png` |
| 6 | Selective-risk CSV | `--figures 6` | `fig6_selective_horizontal.png` |
| 7 | Corrected condition CSV | `--figures 7` | `fig7_nll_readable.png` |
| 9 | Corrected condition CSV | `--figures 9` | `fig8_brier_readable.png` |
| 10 | Corrected condition CSV | `--figures 10` | `fig10_auroc_readable.png` |

Figures 1 and 2 were prepared by the authors in PowerPoint; Figure 3 contains benchmark image examples. These are not represented as Matplotlib data plots here. Figure numbering follows the frozen manuscript, not the historical filenames.

Mendeley Version 1 contains `stage31_condition_results_corrected.csv`, `stage30_four_group_metrics.csv`, `stage30_selective_risk.csv`, `ivc_oxford_calibration_interaction_posthoc.json`, and `ivc_source_transition_posthoc.csv`. The last file is documented for completeness and is not read by these scripts. The plotting inputs and optional interaction input are checked against frozen SHA-256 values; no check should be bypassed.

## Run on CPU

Install Python dependencies and place the published files outside the code directory:

```text
python -m pip install -r environment/requirements.txt
python scripts/figures/plot_figures.py --input-dir PATH_TO_DATA --output-dir PATH_TO_OUTPUT
python scripts/analysis/summarize_aggregates.py --input-dir PATH_TO_DATA --output-dir PATH_TO_OUTPUT --interaction-json PATH_TO_DATA/ivc_oxford_calibration_interaction_posthoc.json
```

Plots are written as PNG and SVG. The analysis script writes aggregate differences and condition-level accuracy; the optional interaction export preserves the input's sign and estimand and does not recompute intervals. Set `RELEASE_DATA_DIR` to the downloaded data directory and run `python -m unittest discover -s tests -v`. Without it, input-dependent tests skip. Tested on Windows using CPython 3.11.2, Matplotlib 3.10.9, NumPy 1.26.3 and Pillow 10.2.0. Different platforms and dependency versions may render differently.

## Licensing and provenance

Project-authored code is licensed under `LICENSE` (MIT). The adapted plotting-style component retains its separate Apache-2.0 licence and attribution in `config/plotting_style/`; it is not relicensed by the project licence. Third-party dependencies retain their own licences. The Mendeley dataset is CC BY 4.0, separate from the code licence. Benchmark images, model weights and other third-party assets are not covered by the project licence.

The plotting scripts are portable adaptations of manuscript figure source code, with source data and scientific plotting logic preserved for the six public figures. See `RELEASE_AUDIT_REPORT.md` for the historical verification record and its limits.
