#pragma once

#include "synak.h"

#define SK_ARRSIZE(ARR)     sizeof(ARR)/sizeof(ARR[0])
#define SK_BUILDTIMESTAMP   std::string(__DATE__) + " " + std::string(__TIME__)

#ifndef _WIN32
    #define SOCKET          int
    #define SOCKET_ERROR    -1
    #define closesocket(s)  ::close(s)
#endif
