/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server Define
* synak_masterserver_define.h
*/

#pragma once

#include "network layer/synak.h"


#define SK_BUILDTIMESTAMP       std::string(__DATE__) + std::string(" ") + std::string(__TIME__)
#define SK_LOG_NFO(...)         SK::MasterServer::LW_writeLog(SK_FILENLINE, SK::MasterServer::eLogType::NFO, ##__VA_ARGS__)
#define SK_LOG_ATT(...)         SK::MasterServer::LW_writeLog(SK_FILENLINE, SK::MasterServer::eLogType::ATT, ##__VA_ARGS__)
#define SK_LOG_ERR(...)         SK::MasterServer::LW_writeLog(SK_FILENLINE, SK::MasterServer::eLogType::ERR, ##__VA_ARGS__)