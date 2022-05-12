/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server
* synak_masterserver.cpp
*/

#include "master server/synak_masterserver.h"


volatile std::atomic_bool SK::MasterServer::m_bRun = false;

/* MasterServer::Initialization
** Initialization the Master Server class
*/
void SK::MasterServer::initialization(int _argc, char *_argv[]) {
    WP_signalBlockAllExcept();


    struct sigaction sigbreak;
    ::sigemptyset(&sigbreak.sa_mask);
    sigbreak.sa_handler = &MasterServer::WP_signalHandler;
    sigbreak.sa_flags = 0;
    if (::sigaction(SIGUSR1, &sigbreak, NULL) != 0)
        SK_WRITELOG(SK_FILENLINE, "ERR", STRERROR);


    if (_argc == 2) {
        nlohmann::json jInitConfig;
        bool bJsonParsed(true);

        try {
            jInitConfig = nlohmann::json::parse(std::string(_argv[1]));
        }
        catch (const std::exception &_e) {
            SK_WRITELOG(SK_FILENLINE, "ERR", "json parse error:", _e.what(), "data:", std::string(jInitConfig));
            bJsonParsed = false;
        }

        if (bJsonParsed
            && jInitConfig.contains("lglv")
            && jInitConfig.contains("ptwp")
            && jInitConfig.contains("ptpl")) {
            try {
                m_LW_iLogLevel = std::stoi(jInitConfig.at("lglv").get<std::string>());
                m_LW_iPort = std::stoi(jInitConfig.at("ptwp").get<std::string>());
                m_GN_iPort = std::stoi(jInitConfig.at("ptpl").get<std::string>());

                SK_WRITELOG(SK_FILENLINE, "NFO", "WebPanel listening port:", std::to_string(m_LW_iPort), "Players listening port:", std::to_string(m_GN_iPort));
            }
            catch (const std::exception &_e) {
                SK_WRITELOG(SK_FILENLINE, "ERR", "std::stoi failed", _e.what(), "data:", std::string(jInitConfig));
            }
        }
    }

    nlohmann::json jCfg;
    jCfg["lglv"] = std::to_string(m_LW_iLogLevel);
    jCfg["ptwp"] = std::to_string(m_LW_iPort);
    jCfg["ptpl"] = std::to_string(m_GN_iPort);
    std::string strCfg(jCfg.dump());
    std::ofstream fCfg("/synak_ms/synak_ms.cfg");
    fCfg.write(strCfg.data(), strCfg.length());


    m_bRun = true;
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
