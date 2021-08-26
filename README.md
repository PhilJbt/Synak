![Synak logo](/public/img/logo.png)

**Synak** is a C++ header-only network library providing networking support for **video games**.\
It can handle **Client/Public Dedicated Server**, **P2P Client/Server** and **full P2P** architecture.\
It also provides a **Master Server** and a **Web Admin Panel** for an Unix dedicated server.

# FEATURES

Feature | Status | Notes
------------ | ------------- | -------------
&#9472; **UDP & TCP** |   |  
&#160; &#9492; Dual-stack IPv4-IPv6 | :heavy_check_mark: |  
&#160; &#9492; Thread safe | :heavy_check_mark: |  
&#160; &#9492; Multiplexer & Demultiplexer | :heavy_multiplication_x: |  
&#160; &#9492; Endianness | :heavy_multiplication_x: |  
&#160; &#9492; Checksum Control | :heavy_multiplication_x: |  
&#160; &#9492; Encryption | :heavy_multiplication_x: |  
&#160; &#9492; Serializing | :heavy_multiplication_x: |  
&#160; &#9492; Ping | :heavy_multiplication_x: |  
&#160; &#9492; Synchronize packet sending | :heavy_multiplication_x: |  
  |   |  
&#9472; **UDP** |   |  
&#160; &#9492; Reliable | :heavy_multiplication_x: |  
&#160; &#9492; Ordered | :heavy_multiplication_x: |  
&#160; &#9492; Hole punching | :heavy_multiplication_x: | Clients P2P Connection
&#160; &#9492; Host migration | :heavy_multiplication_x: | Clients P2P Connection
&#160; &#9492; Keep alive | :heavy_multiplication_x: | TTL reduced
  |   |  
&#9472; **TCP** |   |  
&#160; &#9492; Socket set-up control | :heavy_multiplication_x: | Enable/disable Nagle algorithm, buffers size, etc
  |   |  
&#9472; **MASTER SERVER** |   |  
&#160; &#9492; Port assignation | :heavy_multiplication_x: |  
&#160; &#9492; Matchmaking | :heavy_multiplication_x: |  
&#160; &#9492; IP alias | :heavy_multiplication_x: | Allows to share an endpoint without disclosing its IP address for a P2P connection.<br/>Also useful when showing player's ID on screen.
  |   |  
&#9472; **HTTP** |   |  
&#160; &#9492; Send GET requests | :heavy_multiplication_x: |  
&#160; &#9492; Receive GET answers | :heavy_multiplication_x: |  
&#160; &#9492; Receive POST answers | :heavy_multiplication_x: | POST Arguments supported
&#160; &#9492; Send POST requests | :heavy_multiplication_x: | POST Arguments supported
  |   |  
&#9472; **WEB PORTAL** |   |  
&#160; &#9492; Start & Stop | :heavy_multiplication_x: |  
  |   |  
&#9472; **ALGORITHMS** |   |  
&#160; &#9492; Interpolation | :heavy_multiplication_x: | Distant position
&#160; &#9492; Extrapolation | :heavy_multiplication_x: | Distant position
&#160; &#9492; Prediction | :heavy_multiplication_x: | Local position
&#160; &#9492; Reconciliation | :heavy_multiplication_x: | Local position
