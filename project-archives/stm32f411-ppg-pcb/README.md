# STM32F411 PPG Analog Front-End PCB

## Scope

This KiCad design integrates:

- STM32F411RETx (LQFP64);
- two SFH7070 optical sensors;
- three dual OPA2333 zero-drift amplifiers;
- 5 V input and SPX3819 3.3 V regulation;
- 8 MHz and 32.768 kHz clocks;
- SWD and UART interfaces.

The two analog channels terminate at MCU ADC inputs A0 and A1. The board is a
two-layer design with bottom-side ground copper.

## Design summary

- Approximate outline: 80.6 mm x 52.2 mm
- Modules: 69
- Nets: 83
- Tracks: 602
- Plated holes: 56

## Included files

- `source/Analog.sch` and `source/STM.sch`: hierarchical circuit sheets
- `source/F411_PPG.kicad_pcb`: PCB layout
- `source/F411_PPG.kicad_pro` and legacy project files
- `source/gerber 411_PPG/`: copper, mask, paste, silkscreen, outline, job, and drill outputs

Backups, temporary netlists, caches, and plot-map PostScript files were omitted.

## Limits

The archive reaches schematic, routing, and fabrication-output stages. It does
not include bench-measured waveforms, SNR, filter cutoff, biosignal accuracy,
EMC/thermal results, or automotive qualification.
