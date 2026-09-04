# Solar-Cell Multichannel Measurement and MPPT PCB

## Scope

This archive documents a PADS-based solar-cell measurement design centered on an
STM32F401 mainboard and current/voltage measurement modules. A published
12-channel MPPT data-logger architecture was used as a technical reference.

## Architecture reviewed

```text
12 V input
  -> 5 V and 3.3 V rails
  -> STM32F401 mainboard
  -> three measurement-module connectors
  -> current / voltage analog paths
  -> ADC and DAC
  -> USB/UART
```

The module files expose eight-channel current sensing, an AD7997 ADC, OPA703
voltage paths, and an AD5629R DAC. The parts list and schematic/PCB files allow
the power, reference, sensing, control, and communication nets to be reviewed.

## Included files

- `source/MPPT_module_ver01_260610.sch`
- `source/partslist.xlsx`
- `source/기존ver/VI_measure_MB_ver05_041524.{sch,pcb}`
- `source/기존ver/VI_measure_MDBoard_ver05_041524.{sch,pcb}`

## Reference and attribution

The 12-channel MPPT concept is attributed to Michael D. Kelzenberg, Samuel P.
Loke, and Harry A. Atwater, “Low-cost Open-source 12-channel MPPT Data Logger
for Solar Cell Research,” IEEE PVSC 2021, DOI:
<https://doi.org/10.1109/PVSC43889.2021.9519025>.

The paper PDF, vendor datasheets, installer, and the original author's MPPT12
Gerbers are not mirrored here. The Caltech record is available at:
<https://authors.library.caltech.edu/records/pdfmf-ace76>.

## Limits

The current archive contains design artifacts but no measured accuracy,
efficiency, thermal behavior, or production-yield report. Component values and
reference-rail behavior should be checked against current vendor datasheets
before fabrication.
