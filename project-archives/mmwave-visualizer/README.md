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

## DCA1000EVM troubleshooting

The raw-ADC capture investigation is published as a separate troubleshooting
case because it did not reach the same result as the 3D tracking path.

Observed states:

- Ethernet raw-data capture did not start and board heating was observed.
- mmWave Studio 2.1.0.0 showed FTDI connected while the detected-device count
  remained zero and RS232/SPI remained disconnected.
- RF Power-up produced `ReadRegister failed with error -11` in a retained screen.
- Multiple board status LEDs were photographed before connector, switch, solder,
  power, and accessible signal points were inspected.

Inspection order:

```text
Data path   : IWR6843 raw ADC -> LVDS -> FPGA/buffer -> Ethernet -> PC
Control path: power/mode -> FTDI/RS232/SPI -> reset/config -> capture start
```

Suspicious solder joints were reworked and accessible power/signal points were
checked with an oscilloscope. Raw Ethernet streaming was not restored. Normal
FPGA-buffer reception and a specific failed component were not established, so
the DCA1000 capture path was retired from this test setup.

Public hardware/runtime images are stored under
`src/assets/images/projects/mmwave-visualizer/`:

- `dca1000-setup.webp`
- `dca1000-error-leds.webp`
- `mmwave-studio-readregister-error.webp`

## Limits

- Radar processing and GUI functions are based on TI SDK/Toolbox examples.
- The retained MSS artifact is binary-only, so no MSS source modification is claimed.
- The DCA1000EVM investigation did not restore raw Ethernet streaming or identify
  a failed component.
- Visualizer vital-sign values show functional output, not medical accuracy.
- CAN/LIN, AUTOSAR, and vehicle-network integration were not implemented in this archive.

Large build products, the approximately 1 GB MSS binary, vendor PDFs, and a PPTX
with an unrelated person's name were not published.
