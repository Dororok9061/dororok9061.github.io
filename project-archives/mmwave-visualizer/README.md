# TI mmWave 3D People Tracking Visualizer

## Scope

This archive accompanies a system-integration study using the IWR6843ISK and
IWR6843AOP ecosystem, TI Radar Toolbox examples, Code Composer Studio, and TI
Visualizer applications.

The work covered:

- placement of the radar EVM and adjustment of sensor height/orientation;
- FOV, range, boundary, and threshold configuration;
- review of the C674x DSS/SYS/BIOS build structure;
- review of DSS-to-MSS shared-memory/mailbox data transfer;
- dual-UART setup: CLI at 115200 bps and data at 921600 bps;
- comparison of point-cloud, tracking-box, range-profile, and vital-sign screens.

## Data path

```text
IWR6843 chirps
  -> range / Doppler / angle processing
  -> 2D Capon (MVDR) and dynamic/static CFAR
  -> point cloud and target list
  -> DSS/MSS shared memory and mailbox
  -> serial packet
  -> Visualizer
```

## Included file

- `config/IWR6843AOP.ccxml`: Code Composer Studio target configuration.

## Limits

- Radar processing and GUI functions are based on TI SDK/Toolbox examples.
- The retained MSS artifact is binary-only, so no MSS source modification is claimed.
- Visualizer vital-sign values show functional output, not medical accuracy.
- CAN/LIN, AUTOSAR, and vehicle-network integration were not implemented in this archive.

Large build products, the approximately 1 GB MSS binary, vendor PDFs, and a PPTX
with an unrelated person's name were not published.
