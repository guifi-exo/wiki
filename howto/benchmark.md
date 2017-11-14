disk and CPU benchmark with dd -> src https://romanrm.net/dd-benchmark

Disk benchmark:

    dd bs=1M count=256 if=/dev/zero of=test93722 conv=fdatasync && rm test93722

CPU benchmark:

    if=/dev/zero bs=1M count=1024 | md5sum
