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

- Wireshark showed short UDP configuration packets from `192.168.33.30` to
  `192.168.33.180:4096`, while the raw capture log reported zero received packets.
- UniFlash retained successful SFLASH erase, meta-image download, and program-load
  messages; this was treated as firmware-programming evidence only.
- Tera Term displayed the `mmwDemo:/>` prompt, but several inputs were rejected as
  unrecognized CLI commands.
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

The software-side trace was recorded in this order:

```text
UniFlash program result
  -> Tera Term UART prompt and command response
  -> Wireshark UDP 4096/4098 observation
  -> capture log packet count and raw-file check
  -> mmWave Studio state and hardware inspection
```

The short configuration datagrams were not presented as raw ADC payload. The
zero-packet log and absence of the raw binary remained the capture result.

Suspicious solder joints were reworked and accessible power/signal points were
checked with an oscilloscope. Raw Ethernet streaming was not restored. Normal
FPGA-buffer reception and a specific failed component were not established, so
the DCA1000 capture path was retired from this test setup.

Public hardware/runtime images are stored under
`src/assets/images/projects/mmwave-visualizer/`:

- `dca1000-setup.webp`
- `dca1000-error-leds.webp`

The complete screen sequence is published in the existing DCA1000 article:

- Wireshark and network: `wireshark-ssdp-first-observation.webp`,
  `wireshark-dca-port-filter-empty.webp`, `wireshark-ssdp-repeat.webp`,
  `wireshark-dca-control-udp.webp`, `wireshark-frame-length-filter-empty.webp`,
  `wireshark-dca-bidirectional-udp.webp`, `wireshark-dca-return-udp-detail.webp`,
  `wireshark-dca-response-filter.webp`, `wireshark-udp-ssdp-only.webp`,
  `wireshark-dca-arp-udp-session.webp`, `windows-static-ip-setup.webp`,
  `wireshark-background-udp-traffic.webp`, and
  `wireshark-control-vs-background.webp`.
- UniFlash: `uniflash-program-page.webp` and `uniflash-program-success.webp`.
- Tera Term: `teraterm-cli-command-error.webp`,
  `teraterm-cli-prompt-error.webp`, and `teraterm-serial-character-stream.png`.
- MATLAB and capture result: `matlab-no-binary-files-error.webp`,
  `matlab-record-location-error.webp`, `matlab-configure-radar-error.webp`, and
  `dca1000-zero-packet-log.webp`.
- mmWave Studio: `mmwave-studio-serial-disconnected.webp`,
  `mmwave-studio-readregister-error.webp`, and
  `mmwave-studio-matlab-engine-error.webp`.
- Configuration reference: `dca1000-mode-switch-guide.webp`.

## Limits

- Radar processing and GUI functions are based on TI SDK/Toolbox examples.
- The retained MSS artifact is binary-only, so no MSS source modification is claimed.
- The DCA1000EVM investigation did not restore raw Ethernet streaming or identify
  a failed component.
- Visualizer vital-sign values show functional output, not medical accuracy.
- CAN/LIN, AUTOSAR, and vehicle-network integration were not implemented in this archive.

Large build products, the approximately 1 GB MSS binary, vendor PDFs, and a PPTX
with an unrelated person's name were not published.
