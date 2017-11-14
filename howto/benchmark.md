# dd benchmark

disk and CPU benchmark with dd -> src https://romanrm.net/dd-benchmark

Disk benchmark:

    dd bs=1M count=256 if=/dev/zero of=test93722 conv=fdatasync && rm test93722

CPU benchmark:

    if=/dev/zero bs=1M count=1024 | md5sum

# other

- cpu
    - `stress`
- network
    - `iperf` and `iperf3` (download/upload ~ read/write)
    - `ping` or `mtr` or `traceroute` (latency)
- disk
    - `fio` (read/write)
    - `hdparm` example `sudo hdparm -Tt /dev/sda` (read/write)
    - `ioping` https://github.com/koct9i/ioping#examples (latency)
