/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Network Layer
* main.h
*/

#pragma once

#define _WINSOCKAPI_

// C++
#include <iostream>
#include <ostream>
#include <fstream>
#include <cstring>
#include <stdio.h>
#include <variant>
#include <chrono>
#include <thread>
#include <atomic>
#include <sstream>
#include <iomanip>
#include <ctime>  

// NETWORK
#ifdef _WIN32
    #include <windows.h>
    #include <winsock2.h>
    #include <ws2tcpip.h>
    #include <iphlpapi.h>
    #pragma comment(lib, "Ws2_32.lib")
#else
    #include <sys/types.h>
    #include <sys/socket.h>
    #include <sys/signalfd.h>
    #include <sys/syscall.h>
    #include <sys/epoll.h>
    #include <netinet/in.h>
    #include <netinet/tcp.h>
    #include <arpa/inet.h>
    #include <signal.h>
    #include <unistd.h>
    #include <fcntl.h>
    #include <errno.h>
    #include <csignal>
#endif

// DEPENDENCIES
#define CRCPP_INCLUDE_ESOTERIC_CRC_DEFINITIONS
#include "dependencies/fastCrc32_stephanbrumme/Crc32.h"

#include "dependencies/nlohmann-json-3.10.2/nlohmann/json.hpp"

// SYNAK
#include "network layer/synak_security.h"
#include "network layer/synak_define.h"
#include "network layer/synak_tools.h"
#include "network layer/synak_manager.h"