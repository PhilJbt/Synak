![Synak logo](https://raw.githubusercontent.com/PhilJbt/Synak/main/wiki/logo.png)

```diff
- ⚠️ SYNAK IS STILL IN DEVELOPMENT ⚠️ -
- DO NOT USE IT FOR PRODUCTION IN ITS CURRENT STATE -
```

**Synak** is a network library to connect video game clients together in P2P, written in C++.

### Clients
The liaison between clients is based on **UDP**, with a **client-server P2P architecture** — compatible with nearly all types of **NAT**.

### Master Server
Although optional, a Master Server is provided for a connection with Clients through **TCP** in vue to propose matchmaking or just connections coordination between clients.\
A **Web Admin Panel** is available to facilitate the interraction with it (e.g. to start/stop, to ban/unban IP or UID, to see logs, etc), for an Unix public dedicated server or VPS.\
If the Master Server is not used, the gamer hosting an online game will have to provide the IP address of all players connecting to it - as a whitelist of obfuscated IPs - otherwise the host's NAT will block all connections.


&#160;


[FEATURES](README.md#FEATURES) &#65073; [DEPENDENCIES](README.md#DEPENDENCIES) &#65073; [COMPILER](README.md#COMPILER-SUPPORT) &#65073; [WIKI](wiki/readme.md)
------------ |

&#160;

# FEATURES

### &#9472; LIAISON from CLIENT to CLIENT (UDP)
&#160; &#9492; Dual-stack IPv4-IPv6\
&#160; &#9492; Thread safe\
&#160; &#9492; Packet checksum control *(CRC-32)*\
&#160; &#9492; Packet payload compression `FORTHCOMING v1.5`\
&#160; &#9492; Reliable packet delivery\
&#160; &#9492; Ordered packets\
&#160; &#9492; Spoofed packet source addresses mitigation\
&#160; &#9492; Multiplexer & demultiplexer `FORTHCOMING v1.0`\
&#160; &#9492; Synchronize one-time event packets reception `FORTHCOMING v1.1`\
&#160; &#9492; Packet payload serializing\
&#160; &#9492; Packet payload obfuscation\
&#160; &#9492; Big & little-endianness support `TBC`\
&#160; &#9492; Ping\
&#160; &#9492; Keep alive\
&#160; &#9492; Hole punching\
&#160; &#9492; Socket options *(change buffers size, etc)*\
&#160; &#9492; IP alias *(Obfuscation of IP for connections between Clients in case the Master Server is not used.)* `FORTHCOMING v1.0`\
&#160; &#9492; Host migration `FORTHCOMING v1.3`

### &#9472; CLIENT
&#160; &#9492; Interpolation *(remote player)* `FORTHCOMING 1.1`\
&#160; &#9492; Extrapolation *(remote player)* `FORTHCOMING 1.1`\
&#160; &#9492; Prediction *(local player)* `FORTHCOMING 1.6`\
&#160; &#9492; Reconciliation *(local player)* `FORTHCOMING 1.6`\
&#160; &#9492; Send HTTP GET requests `FORTHCOMING v1.4`\
&#160; &#9492; Receive HTTP GET answers `FORTHCOMING v1.4`\
&#160; &#9492; Send HTTP POST requests `FORTHCOMING v1.4`\
&#160; &#9492; Receive HTTP POST answers `FORTHCOMING v1.4`

### &#9472; LIAISON from MASTER SERVER to CLIENT (TCP)
&#160; &#9492; Dual-stack IPv4-IPv6\
&#160; &#9492; Thread safe\
&#160; &#9492; Packet checksum control *(CRC-32)*\
&#160; &#9492; Socket options *(enable/disable Nagle algorithm, change buffers size, etc)*\\
&#160; &#9492; Spoofed packet source addresses mitigation\
&#160; &#9492; Big & little-endianness support `TBC`\
&#160; &#9492; Port assignation\
&#160; &#9492; Session ID\
&#160; &#9492; Matchmaking

### &#9472; LIAISON from MASTER SERVER to WEB PANEL (TCP)
&#160; &#9492; Socket options *(enable/disable Nagle algorithm, change buffers size, etc)*\
&#160; &#9492; Statistics

### &#9472; WEB PANEL
&#160; &#9492; Logs\
&#160; &#9492; Start, Stop/Kill\
&#160; &#9492; Ban / Unban IPv4/v6\
&#160; &#9492; Ban / Unban UID\
&#160; &#9492; Master Server statistics\
&#160; &#9492; Dedicated server optimization reporter

&#160;

# COMPILER SUPPORT

Type | Compiler | Version
------------ | ------------ | ------------
Network Layer | MSVC | 2022 (v143)
Master Server | g++ | 9.3

Standard version: C++20

&#160;

# DEPENDENCIES

- **Network Layer** / **Master Server**
  - [nlohmann-json-3.10.2](https://github.com/nlohmann/json) (included)
  - [Fast CRC32 7a028136d54f8fe93b7cf533ca098f0bf30c3fbd](https://github.com/stbrumme/crc32) (included)

&#160;

- **Web Panel**
  - Tmux ≥1.8
  - Apache ≥2.0
    - mod_cgi
    - mod_cgid
    - mod_env
    - mod_rewrite
  - Python ≥3.0
  - [Semantic UI 2.4](https://semantic-ui.com/) (included)
    - Google Font dependency bypassed
