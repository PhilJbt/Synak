/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Network Layer
* main.h
*/

#pragma once

#define _WINSOCKAPI_

// C++
#include <iostream>
#include <cstring>
#include <stdio.h>
#include <variant>
#include <thread>
#include <atomic>

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
    #include <signal.h>
    #include <netinet/in.h>
    #include <netinet/tcp.h>
    #include <arpa/inet.h>
    #include <unistd.h>
    #include <fcntl.h>
    #include <errno.h>
    #include <csignal>
#endif

// DEPENDENCIES
#include <dependencies/nlohmann-json-3.10.2/nlohmann/json.hpp>
using json = nlohmann::json;

// SYNAK
#include <network layer/synak_define.h>
#include <network layer/synak_manager.h>
#include <master server/synak_masterserver.h>
