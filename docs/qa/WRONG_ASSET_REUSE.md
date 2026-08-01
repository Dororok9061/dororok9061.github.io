# Wrong Asset Reuse Audit

This record covers the current working tree on `rebuild/source-faithful-site-notion-github`.

## Current result

- 358 static public asset references resolve to 122 source or pinned-theme files.
- All eleven coursework primary covers exist under `/assets/images/study/coursework/`.
- The eleven coursework covers have eleven distinct SHA-256 hashes.
- Electronic Circuits I, Electronic Circuits II, Digital Communications, and Power Electronics now use self-authored concept maps instead of cross-project visuals.
- The Embedded Systems course uses `embedded-systems-source-map.svg`, not a Raspberry Pi or STM32 project photograph.
- The Embedded Systems record has no fabricated weekly units and links separately to STM32 study, FMCW acquisition, and the Raspberry Pi prototype.

## Repaired contextual covers

The four primary covers that previously reused nearby project visuals were replaced with self-authored maps scoped to each course:

- Electronic Circuits I maps diode behavior, biasing, and a common-emitter amplifier.
- Electronic Circuits II maps a differential input, feedback, filtering, and an output stage.
- Digital Communications maps sampling through decoding in a transmitter-to-receiver chain.
- Power Electronics maps controlled switching and energy storage from a DC source to a load.

No contextual project or cross-course visual remains as a primary coursework cover. These maps are navigation artwork, not proof of course completion; the course records retain `study-roadmap` or source-boundary wording where applicable.

## STM32 boundary

The earlier STM32 route incorrectly reused a PCB-inspection asset family. Those inspection images and descriptions are no longer referenced by STM32 pages.

The corrected track uses twenty-two prototype photographs, a forty-slide setup deck, a three-page KiCad schematic, and the saved CubeIDE/firmware archive. Eight track pages connect the NUCLEO-F411RE hardware, ECG/PPG analog front end, ADC/TIM1/USART2 path, CMSIS-DSP filters, and peak/HRV code. Photographs confirm the physical prototype only; they are not presented as measured waveform quality or accuracy evidence.

## Regression commands

```text
python scripts/content/check_asset_provenance.py
python scripts/content/check_category_asset_match.py
python scripts/content/check_duplicate_cover_usage.py
python scripts/content/check_hardware_name_match.py
```
