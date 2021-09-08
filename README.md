![Synak logo](https://repository-images.githubusercontent.com/400254624/3b6e9edf-f5af-4c4f-8012-73436cdfd43d)

**Synak** is a C++ library providing networking support for **video games**.\
It can handle **Client/Public Server** and **P2P** architectures — even behind a NAT.\
It also provides a **Master Server** (for matchmaking, to coordinate connection between P2P nodes, etc) and a **Web Admin Panel** (to start/stop, to ban/unban, for logs, etc) for an Unix public dedicated server.

&#160;


[FEATURES](README.md#FEATURES) &#65073; [DEPENDENCIES](README.md#DEPENDENCIES) &#65073; [WIKI](wiki/readme.md)
------------ |

&#160;

# FEATURES

Feature | Status | Notes
------------ | ------------- | -------------
&#9472; **UDP & TCP** |   |  
&#160; &#9492; Dual-stack IPv4-IPv6 | :heavy_check_mark: |  
&#160; &#9492; Thread safe | :heavy_check_mark: |  
&#160; &#9492; Multiplexer & Demultiplexer | :construction: |  
&#160; &#9492; Endianness | :construction: |  
&#160; &#9492; Checksum Control | :construction: |  
&#160; &#9492; Encryption | :construction: |  
&#160; &#9492; Serializing | :construction: |  
&#160; &#9492; Ping | :construction: |  
&#160; &#9492; Synchronize packet sending | :construction: |  
&#160; &#9492; Compression | :construction: |  
  |   |  
&#9472; **UDP** |   |  
&#160; &#9492; Reliable | :construction: |  
&#160; &#9492; Ordered | :construction: |  
&#160; &#9492; Hole punching | :construction: | P2P only
&#160; &#9492; Host migration | :construction: | P2P only
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

# DEPENDENCIES

- **Network Layer** / **Master Server**
  - [nlohmann-json-3.10.2](https://github.com/nlohmann/json) (included)
  - [CRCpp](https://github.com/d-bahr/CRCpp) (included)

&#160;

- **Web Panel**
  - Tmux ≥1.8
  - Apache ≥2.0
    - mod_rewrite
  - Python ≥3.0
  - [Semantic UI](https://semantic-ui.com/) (included)
  - [crc32.py](https://gist.github.com/cholcombe973/a0af818d212e58ae151c) (included)
