/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server
* synak_masterserver.cpp
*/

#include "master server/synak_masterserver.h"


volatile std::atomic_bool SK::MasterServer::m_bRun = false;
SK::MasterServer::eLogType SK::MasterServer::m_LW_eLogLevel = SK::MasterServer::eLogType::ERR;


/* MasterServer::Initialization
** Initialization the Master Server class
*/
void SK::MasterServer::initialization(int _argc, char *_argv[]) {
    // Flush log
    LW_flushLog();

    // Block all signals on this thread
    WP_signalBlockAllExcept();

    // Bind MasterServer::WP_signalHandler() to the SIGUSR1 signal
    // Used for clean threads stop
    struct sigaction sigbreak;
    ::sigemptyset(&sigbreak.sa_mask);
    sigbreak.sa_handler = &MasterServer::WP_signalHandler;
    sigbreak.sa_flags = 0;
    if (::sigaction(SIGUSR1, &sigbreak, NULL) != 0)
        SK_LOG_ERR(STRERROR);

    // Load configuration file for listening ports and log level values
    if (_argc == 2) {
        nlohmann::json jInitConfig;
        bool bJsonParsed(true);

        try {
            jInitConfig = nlohmann::json::parse(std::string(_argv[1]));
        }
        catch (const std::exception &_e) {
            SK_LOG_ERR("json parse error:", _e.what(), "data:", std::string(jInitConfig));
            bJsonParsed = false;
        }

        if (bJsonParsed
            && jInitConfig.contains("lglv")
            && jInitConfig.contains("ptwp")
            && jInitConfig.contains("ptpl")) {
            bool bApplyLoadedValues(true);
            int iLogLevel_tmp(0),
                iPanelPort_tmp(0),
                iGamePort_tmp(0);

            try {
                iLogLevel_tmp = std::stoi(jInitConfig.at("lglv").get<std::string>());
                iPanelPort_tmp = std::stoi(jInitConfig.at("ptwp").get<std::string>());
                iGamePort_tmp = std::stoi(jInitConfig.at("ptpl").get<std::string>());
            }
            catch (const std::exception &_e) {
                SK_LOG_ERR("std::stoi failed", _e.what(), "data:", std::string(jInitConfig));
                bApplyLoadedValues = false;
            }

            if (bApplyLoadedValues) {
                m_LW_eLogLevel = static_cast<SK::MasterServer::eLogType>(iLogLevel_tmp);
                m_WP_iPort = iPanelPort_tmp;
                m_IG_iPort = iGamePort_tmp;
            }
        }
    }
    
    // Write configuration file
    configBackup();

    // Allow threads to stay opened
    m_bRun = true;

    // Write startup log
    SK_LOG_NFO(
        "Starting Synak MS.",
        std::string("BUILD: " + SK_BUILDTIMESTAMP),
        std::string("LOG LEVEL: INFORMATION"), // This message will only be visibile if LOG LEVEL is INFORMATION, so...
        std::string("WEB PANEL LISTENING PORT: " + std::to_string(m_WP_iPort)),
        std::string("PLAYERS LISTENING PORT: " + std::to_string(m_IG_iPort))
    );
}

/* MasterServer::configBackup
** Save the configuration into a text file
*/
void SK::MasterServer::configBackup() {
    nlohmann::json jCfg;
    jCfg["lglv"] = std::to_string(static_cast<int>(m_LW_eLogLevel));
    jCfg["ptwp"] = std::to_string(m_WP_iPort);
    jCfg["ptpl"] = std::to_string(m_IG_iPort);

    std::string strCfg(jCfg.dump());

    std::ofstream fCfg("/synak_ms/synak_ms.cfg");
    fCfg.write(strCfg.data(), strCfg.length());
    fCfg.close();
}

/* MasterServer::Unitialization
** Clean the Master Server class
*/
void SK::MasterServer::desinitialization() {
    m_bRun = false;

    // Close the terminal watcher thread
    if (m_WP_thdWatcherTerminal) {
        m_WP_thdWatcherTerminal->join();
        delete m_WP_thdWatcherTerminal;
        m_WP_thdWatcherTerminal = nullptr;
    }

    // Close the webpanel watcher thread
    if (m_WP_thdWatcherWebpanel) {
        m_WP_thdWatcherWebpanel->join();
        delete m_WP_thdWatcherWebpanel;
        m_WP_thdWatcherWebpanel = nullptr;
    }
    SK_CLOSESOCKET(m_WP_sckfd);

    // Close shutdown pipe notification
    ::close(m_WP_fdPipeKill[0]);
    ::close(m_WP_fdPipeKill[1]);
}
