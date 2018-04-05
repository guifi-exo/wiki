# network logging

Network Logging

    config system
    (...)
        option log_ip <rsyslog IP>

more log_* options https://openwrt.org/docs/guide-user/base-system/system_configuration

general guide http://bredsaal.dk/debian-rsyslog-server-with-openwrt-rsyslog-client

note: I recommend adding these lines in /etc/rsyslog.conf

    # separate log files by host name of sending device
    # src http://www.rsyslog.com/article60/
    $template DynaFile,"/var/log/system-%HOSTNAME%.log"
    *.* -?DynaFile

src https://openwrt.org/docs/guide-user/troubleshooting/log.essentials#network_logging

# reset device

    jffs2reset

# back to original firmware

    cd /tmp
    wget http://www.example.org/original_firmware.bin
    mtd -r write /tmp/original_firmware.bin firmware

src https://wiki.openwrt.org/doc/howto/generic.uninstall
