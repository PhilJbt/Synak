![Synak logo](https://raw.githubusercontent.com/PhilJbt/Synak/main/wiki/logo.png)

&#160;

# MENU

| [WIKI](wiki/readme.md) |
:----------------------------------------------------------: |
| [I. PRESENSATION](README.md#i-presensation) &#65293; [II. FEATURES](README.md#ii-features) &#65293; [III. SPECIFICATIONS](README.md#iii-specifications) &#65293; [IV. COMPILER](README.md#iv-compiler-support) &#65293; [V. DEPENDENCIES](README.md#v-dependencies) |



&#160;

```diff
- ⚠️ STILL IN DEVELOPMEN, DO NOT USE IT FOR PRODUCTION IN ITS CURRENT STATE ⚠️ -
```

#### **Synak** is a network library written in C++ providing a connection between multiple video game clients in P2P, through an optional third point.

&#160;

# I. PRESENSATION

The liaison between clients is based on **UDP**, with a **client-server P2P architecture** — compatible with nearly all types of **NAT**.

Although optional, a Master Server is provided for a connection with Clients through **TCP** in vue to propose matchmaking or just connections coordination between clients.\
A **Web Admin Panel** is available to facilitate the interraction with it (e.g. to start/stop, to ban/unban IP or UID, to see logs, etc), for an Unix public dedicated server or VPS.\
If the Master Server is not used, the gamer hosting an online game will have to provide the IP address of all players connecting to it - as a whitelist of obfuscated IPs - otherwise the host's NAT will block all connections.

###### [Return to menu](README.md#menu)

&#160;

# II. FEATURES

### &#9472; CLIENT
* Memory scanner variables mitigation `FORTHCOMING v1.0`
* IP alias *(Obfuscation of IP for connections between Clients in case the Master Server is not used)* `FORTHCOMING v1.0`
* Interpolation *(remote player)* `FORTHCOMING 1.1`
* Extrapolation *(remote player)* `FORTHCOMING 1.1`
* Host migration `FORTHCOMING v1.3`
* Send & receive HTTP GET/POST requests `FORTHCOMING v1.4`
* Prediction *(local player)* `FORTHCOMING 1.6`
* Reconciliation *(local player)* `FORTHCOMING 1.6`

&#160;

### &#9472; MASTER SERVER
* Port assignation
* Session ID *(To join a private session)*
* Matchmaking

&#160;

### &#9472; WEB PANEL
* Statistics
* Logs
* Start, Stop/Kill
* Ban / Unban IPv4/v6
* Ban / Unban UID *(Volume UID by default, can be overridden)*
* Dedicated server optimization reporter

###### [Return to menu](README.md#menu)

&#160;

# III. SPECIFICATIONS

* Dual-stack IPv4-IPv6
* Thread safe
* Packet checksum control *(CRC-32)*
* Reliable packet delivery
* Ordered packets
* Spoofed packet source addresses mitigation
* Ping
* Keep alive
* Socket options *(enable/disable Nagle algorithm for TCP, change buffers size for TCP and UDP, etc)*
* Hole punching (UDP)
* Packet payload serializing
* Packet payload encryption *(BLOWFISH and RSA)*
* Packet payload compression `FORTHCOMING v1.5`
* Multiplexer & demultiplexer `FORTHCOMING v1.0`
* Synchronize one-time event packets reception `FORTHCOMING v1.1`
* Big & little-endianness support `TBC`

###### [Return to menu](README.md#menu)

&#160;

# IV. COMPILER SUPPORT

Standard version: C++20

### &#9472; NETWORK LAYER
  * MSVC
    * v143 (2022)

### &#9472; MASTER SERVER
  * g++
    * v9.3
    * v10.0

###### [Return to menu](README.md#menu)

&#160;

# V. DEPENDENCIES

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
    * Google Font dependency has been manually bypassed

###### [Return to menu](README.md#menu)
