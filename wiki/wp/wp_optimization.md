# DEDICATED SERVER OPTIMIZATIONS APPLICATION

These are only optional optimizations and are not mandatory, you can either temporarily or permanently patch these values.

* To manually get current values, type `sysctl -n <CONFIG_OPTION_NAME>` or `cat <CONFIG_OPTION_PATH` in your terminal.

For example:
```
root@yourdedi:/# sysctl -n net.ipv4.ip_local_port_range
15000   61000
root@yourdedi:/# cat /proc/sys/net/ipv4/tcp_syncookies
1
```

&#160;

## I. Temporary mode

With the temporary mode, just <b>REBOOT</b> your dedicated server will rollback everything in the previous state.

* Type `sudo sysctl -w <CONFIG_OPTION_NAME>=<DESIRED_VALUE>` in your terminal to apply changes.

For example:

```
root@yourdedi:/# sysctl -n net.ipv4.tcp_syncookies=1
net.ipv4.tcp_syncookies = 1
root@yourdedi:/# sysctl -n net.ipv4.ip_local_port_range='15000 61000'
net.ipv4.ip_local_port_range = 15000 61000
```

&#160;

## II. Permanent mode

With the permanent mode, you need to remove or comment (add a '_#_' character at the beginning of the line) options you added in an option file to rollback options in an earlier state.

* Type `nano /etc/sysctl.conf` in your terminal to edit the config file
* Go to the end of the file by pressing the `PAGE DOWN` keyboard key several times
* On a new line, write each desired options in the form `<CONFIG_OPTION_NAME>=<DESIRED_VALUE>`
* Save and close with `CTRL+X` then `Y` and `ENTER` keyboard keys
* Type `sysctl -p` to load the configuration file

&#160;

## III. The net.ipv4.tcp_congestion_control special case

Google developed a new TCP Congestion Control Algorithm which overcomes many of the Reno and CUBIC issues (the usual default CCAs), improving bandwidth usage and reducing latency.

To use Google's **BBR TCP Congestion Control** as default CCA:

* Type `uname -r` in your terminal, and check your kernel version is **4.9 or newer**
  * :x: If it is **NOT** the case, **DO NOT** continue and try to update your kernel
  * :heavy_check_mark: If it is the case, you can continue the steps below
* Type `sudo nano /etc/sysctl.conf` to edit the config file
* Go to the end of the file by pressing the `PAGE DOWN` keyboard key several times
* Add the two lines `net.core.default_qdisc=fq` and `net.ipv4.tcp_congestion_control=bbr` at the bottom of the file
* Save and close with `CTRL+X` then `Y` and `ENTER` keyboard keys
* Load the new configuration with the command `sudo sysctl -p`
* Finally, check which congestion control algorithm is in use with the command `sysctl net.ipv4.tcp_congestion_control`
