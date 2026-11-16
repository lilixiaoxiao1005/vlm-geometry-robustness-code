# Historical local release acceptance record

The statuses and authorisations below describe the time this audit was performed; they are not a statement of present or future release status.

Project-authored code is MIT licensed, copyright 2026 Li Ruolei and Ru Yaohui. The adapted plotting style retains its separate Apache-2.0 licence and attribution; these are not relicensed. Mendeley Data Version 1 is CC BY 4.0, which applies to the dataset separately from the code. At the time of this audit, no public upload had been authorised.

## Public input and figure limits

The five Version 1 files were downloaded from the official Mendeley endpoint in the previous closure and all five SHA-256 hashes matched the frozen manifest. This historical download was not repeated in this finalization. The currently available downloaded public files were used for this round's tests. Figure 8 and Supplementary Figure S1 require an additional author-controlled aggregate input not included in public Mendeley Version 1. That input is not approved for release and was not read or used during this round. It cannot provide a full source-level Bootstrap rerun.

The previous closure recorded an eight-figure pixel comparison using additional author-controlled aggregate input. That is historical evidence only; this round rechecked **six figures from public inputs**. Figures 4, 5, 6, 7, 9 and 10 each reproduced the frozen manuscript PNG pixel-for-pixel in the existing previously created Windows virtual environment, and their PNG and SVG files passed integrity/parsing checks. This is not a cross-platform guarantee.

## This round's verification

- Standard MIT licence text and the specified two-author copyright notice were added.
- The existing Apache licence and third-party notice remain byte-for-byte unchanged from before this round.
- Four release smoke tests passed. Two previous sensitivity-specific checks were replaced with tests for rejection of a modified public input and rejection of unsupported figure selections, matching the public-only scope. The original output is in `RELEASE_SMOKE_TEST_OUTPUT.txt`.
- Python 3.11.2, Matplotlib 3.10.9, NumPy 1.26.3 and Pillow 10.2.0 were used in the previously verified clean virtual environment. A new environment was not installed this round; clean installation is historical evidence from the prior closure.
- Public input hashes are checked by the plotting and aggregation scripts. Manifest inventory and SHA-256 list were regenerated for the proposed public file set, with manifest and checksum self-reference rules explicitly stated.
- No paper manuscript, figure, frozen dataset, Mendeley record or third-party licence text was changed. No private per-source data, benchmark images, labels, model weights or GPU were accessed. No experiment or public upload was performed.

## Historical status at the time of this audit

```ini
PROJECT_CODE_LICENSE = MIT
THIRD_PARTY_LICENSE_PRESERVATION = PASS
PUBLIC_DATA_LICENSE = CC_BY_4_0
ECE_AGGREGATE_PUBLICATION_STATUS = NOT_AUTHORIZED
PUBLIC_FIGURE_REPRODUCIBILITY = 6_OF_6_PIXEL_IDENTICAL
CLEAN_ENVIRONMENT_TEST = PASS_EXISTING_PREVIOUSLY_VERIFIED_ENVIRONMENT
RELEASE_MANIFEST_CONSISTENCY = PASS
SHA256_INTEGRITY = PASS
LOCAL_RELEASE_CANDIDATE_READY = YES
PUBLIC_RELEASE_AUTHORIZED = NO
NEW_EXPERIMENTS = 0
GPU_FORWARDS = 0
```

At the time of this audit, the code candidate was ready for author review and public release had not been authorised. The input excluded above remains author-controlled.
