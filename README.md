![Synak logo](https://raw.githubusercontent.com/PhilJbt/Synak/main/wiki/logo.png)

**Synak** is a C++ library providing networking support for **video games**.

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

Feature | Status | Notes
------------ | ------------- | -------------
&#9472; **UDP & TCP** |   |  
&#160; &#9492; Dual-stack IPv4-IPv6 | :construction: |  
&#160; &#9492; Thread safe | :construction: |  
&#160; &#9492; Checksum Control | :heavy_check_mark: | CRC-32   
&#160; &#9492; Serializing | :construction: |  
&#160; &#9492; Big / Little-Endianness Support | :construction: |  
&#160; &#9492; Packet Obfuscation | :construction: |  
&#160; &#9492; Compression | :construction: |  
&#160; &#9492; Multiplexer & Demultiplexer | :construction: |
&#160; &#9492; Ping | :construction: |  
&#160; &#9492; Synchronize packet sending | :construction: |  
  |   |  
&#9472; **UDP** |   |  
&#160; &#9492; Reliable | :construction: |  
&#160; &#9492; Ordered | :construction: |  
&#160; &#9492; Hole punching | :construction: |  
&#160; &#9492; Host migration | :construction: |  
&#160; &#9492; Keep alive | :construction: | TTL reduced
  |   |  
&#9472; **TCP** |   |  
&#160; &#9492; Socket options | :construction: | Enable/disable Nagle algorithm, buffers size, etc
  |   |  
&#9472; **MASTER SERVER** |   |  
&#160; &#9492; Port assignation | :construction: |  
&#160; &#9492; Matchmaking | :construction: |  
&#160; &#9492; IP alias | :construction: | Obfuscate endpoint IP for P2P connections
  |   |  
&#9472; **HTTP** |   |  
&#160; &#9492; Send GET requests | :construction: |  
&#160; &#9492; Receive GET answers | :construction: |  
&#160; &#9492; Receive POST answers | :construction: | POST Arguments supported
&#160; &#9492; Send POST requests | :construction: | POST Arguments supported
  |   |  
&#9472; **WEB PORTAL** |   |  
&#160; &#9492; Logs | :heavy_check_mark: |  
&#160; &#9492; Start, Stop/Kill | :heavy_check_mark: |  
&#160; &#9492; Ban / Unban IPv4/v6 | :heavy_check_mark: |  
&#160; &#9492; Master Server statistics | :heavy_check_mark: |  
&#160; &#9492; Dedicated Server optimizations | :heavy_check_mark: |  
  |   |  
&#9472; **ALGORITHMS** |   |  
&#160; &#9492; Interpolation | :construction: | Distant position
&#160; &#9492; Extrapolation | :construction: | Distant position
&#160; &#9492; Prediction | :construction: | Local position
&#160; &#9492; Reconciliation | :construction: | Local position

&#160;

# COMPILER SUPPORT

Compiler | Version
------------ | ------------ 
Visual Studio | 2019 (v142)
g++ | 9.3

Standard version: C++17

&#160;

# DEPENDENCIES

- **Network Layer** / **Master Server**
  - [nlohmann-json-3.10.2](https://github.com/nlohmann/json) (included)
  - [CRCpp 1.1.0.0](https://github.com/d-bahr/CRCpp) (included)

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
  - [crc32.py 7/11/15](https://gist.github.com/cholcombe973/a0af818d212e58ae151c) (included)
