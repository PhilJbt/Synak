/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server Define
* synak_masterserver_define.h
*/

#pragma once

#include <network layer/synak.h>



#define SK_BUILDTIMESTAMP       std::string(__DATE__) + " " + std::string(__TIME__)
#define SK_WRITELOG             MasterServer::writeLog
