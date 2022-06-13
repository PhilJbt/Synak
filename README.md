![Synak logo](https://raw.githubusercontent.com/PhilJbt/Synak/main/wiki/logo.png)

```diff
- ⚠️ SYNAK IS STILL IN DEVELOPMENT ⚠️ -
- DO NOT USE IT FOR PRODUCTION IN ITS CURRENT STATE -
```

**Synak** is a network library to connect video game clients together in P2P, written in C++.

&#160;

### &#9472; Clients
The liaison between clients is based on **UDP**, with a **client-server P2P architecture** — compatible with nearly all types of **NAT**.

&#160;

### &#9472; Master Server
Although optional, a Master Server is provided for a connection with Clients through **TCP** in vue to propose matchmaking or just connections coordination between clients.\
A **Web Admin Panel** is available to facilitate the interraction with it (e.g. to start/stop, to ban/unban IP or UID, to see logs, etc), for an Unix public dedicated server or VPS.\
If the Master Server is not used, the gamer hosting an online game will have to provide the IP address of all players connecting to it - as a whitelist of obfuscated IPs - otherwise the host's NAT will block all connections.

&#160;

[WIKI](README.md#WIKI) &#65073; [FEATURES](README.md#FEATURES) &#65073; [DEPENDENCIES](README.md#DEPENDENCIES) &#65073; [COMPILER](README.md#COMPILER-SUPPORT)
------------ |

&#160;

# WIKI

Please refer directly to the [Wiki](wiki/readme.md) page.

&#160;

# FEATURES

### &#9472; LIAISON from CLIENT to CLIENT (UDP)
* Dual-stack IPv4-IPv6
* Thread safe
* Packet checksum control *(CRC-32)*
* Packet payload compression `FORTHCOMING v1.5`
* Reliable packet delivery
* Ordered packets
* Spoofed packet source addresses mitigation
* Multiplexer & demultiplexer `FORTHCOMING v1.0`
* Synchronize one-time event packets reception `FORTHCOMING v1.1`
* Packet payload serializing
* Packet payload obfuscation
* Big & little-endianness support `TBC`
* Ping
* Keep alive
* Hole punching
* Socket options *(change buffers size, etc)*
* IP alias *(Obfuscation of IP for connections between Clients in case the Master Server is not used.)* `FORTHCOMING v1.0`
* Host migration `FORTHCOMING v1.3`

&#160;

### &#9472; CLIENT
* Interpolation *(remote player)* `FORTHCOMING 1.1`
* Extrapolation *(remote player)* `FORTHCOMING 1.1`
* Prediction *(local player)* `FORTHCOMING 1.6`
* Reconciliation *(local player)* `FORTHCOMING 1.6`
* Send HTTP GET requests `FORTHCOMING v1.4`
* Receive HTTP GET answers `FORTHCOMING v1.4`
* Send HTTP POST requests `FORTHCOMING v1.4`
* Receive HTTP POST answers `FORTHCOMING v1.4`

&#160;

### &#9472; LIAISON from MASTER SERVER to CLIENT (TCP)
* Dual-stack IPv4-IPv6
* Thread safe
* Packet checksum control *(CRC-32)*
* Socket options *(enable/disable Nagle algorithm, change buffers size, etc)*\
* Spoofed packet source addresses mitigation
* Big & little-endianness support `TBC`
* Port assignation
* Session ID
* Matchmaking

&#160;

### &#9472; LIAISON from MASTER SERVER to WEB PANEL (TCP)
* Socket options *(enable/disable Nagle algorithm, change buffers size, etc)*
* Statistics

&#160;

### &#9472; WEB PANEL
* Logs
* Start, Stop/Kill
* Ban / Unban IPv4/v6
* Ban / Unban UID
* Master Server statistics
* Dedicated server optimization reporter

&#160;

# COMPILER SUPPORT

Standard version: C++20

### &#9472; NETWORK LAYER
  * MSVC
    * v143 (2022)

### &#9472; MASTER SERVER
  * g++
    * 9.3
    * 10.0

&#160;

# DEPENDENCIES

### &#9472; Network Layer / Master Server
  * [nlohmann-json-3.10.2](https://github.com/nlohmann/json) (included)
  * [Fast CRC32 7a028136d54f8fe93b7cf533ca098f0bf30c3fbd](https://github.com/stbrumme/crc32) (included)

&#160;

### &#9472; Web Panel
  * Tmux ≥1.8
  * Apache ≥2.0
    * mod_cgi
    * mod_cgid
    * mod_env
    * mod_rewrite
  * Python ≥3.0
  * [Semantic UI 2.4](https://semantic-ui.com/) (included)
    * Google Font dependency bypassed
