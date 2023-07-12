## Logging/monitoring server on aarch64 archlinux Raspberry Pi with Ansible

```
  +---------------+           +---------------+           +---------------+
  |   journald    |           |   Exporters:  |           |  pgw_scripts  |
  +---------------+           |  -----------  |           +---------------+ 
          |                   |    node       |                   |
          |                   |    systemd    |                   |
          V                   |    influx     |                   |
  +---------------+           +---------------+                   |
  |   Syslog-ng   |                   |                           |
  +---------------+                   |                           |
          |                           |                           |
          |                           |                           |
          V                           V                           V
  +---------------+           +---------------+           +---------------+
  |   Telegraf    |           |  Prometheus   |  <------  |  Pushgateway  | 
  +---------------+           +---------------+           +---------------+
          |                           |
          |                           |
          V                           V
  +---------------+           +---------------+
  |   InfluxDB    |  ------>  |    Grafana    |
  +---------------+           +---------------+
```

This setup has zero security and zero redundancy. It's meant to be minimal, take up as little space as possible and handle inconsequential data.

If needed:
* use ansible-vault for encrypted passwords or use key based access.
* self-signed TLS for services.
* Prometheus and influxdb replication / HA

### Some configuration details

Prometheus tsdb retention is the default 2 weeks.

The telegraf database in InfluxDB has a retention policy of 2 weeks.

prometheus-node-exporter is run with ignore flag for cifs filesystems.
When a windows shared folder is mounted and the machine goes offline, node-exporter will keep working.

Logrotate is set to keep 1 days worth of backlogs, and rotates daily.

Journald is configured to use no more than 1G of disk space. This could be lowered more, as syslog-ng pulls messages from journald effectively instantaneously.

There are two scripts that utilize pushgateway:
* pgw_exporter:
  * cpu usage by process
  * memory usage by process
  * process count
  * pinger
* pgw_pkgs
  * package updates

### Pics

![image](https://github.com/jp1995/rpi-monitor/assets/8545997/6d2d2448-d680-499b-806a-ec5658fd535f)

![image](https://github.com/jp1995/rpi-monitor/assets/8545997/78f0dabe-d11f-4bfa-97d6-2ffbc6fc21f9)
