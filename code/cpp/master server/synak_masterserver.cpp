/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server
* synak_masterserver.cpp
*/

#include <network layer/synak.h>


/* MasterServer::Initialization
** Initialization the Master Server class
*/
void MasterServer::initialization() {
    m_bRun = true;
}

/* MasterServer::Unitialization
** Clean the Master Server class
*/
void MasterServer::unitialization() {
    m_bRun = false;

    // Close the terminal watcher thread
    if (m_thdWatcherTerminal) {
        m_thdWatcherTerminal->join();
        delete m_thdWatcherTerminal;
        m_thdWatcherTerminal = nullptr;
    }

    // Close the webpanel watcher thread
    if (m_thdWatcherWebpanel) {
        m_thdWatcherWebpanel->join();
        delete m_thdWatcherWebpanel;
        m_thdWatcherWebpanel = nullptr;
    }
    SK_CLOSESOCKET(m_sckfdWP);
}

/* MasterServer::Stop
** Close all Master Server modules
*/
void MasterServer::stop() {
    m_bRun = false;
}

/* MasterServer::WatcherTerminal
** Launch the threaded Terminal Watcher
*/
void MasterServer::watcherTerminal() {
    if (!m_thdWatcherTerminal)
        m_thdWatcherTerminal = new std::thread(&MasterServer::_watcherterminal, this);
}

/* MasterServer::_watcherterminal
** Monitors for an keyboard input in the terminal
*/
void MasterServer::_watcherterminal() {
    SynakManager::signalBlockAll();

    // Initialize input command string
    std::string strCmd;
    
    // Check commands written in the terminal
    fd_set   fdsr;
    timespec ts;
    ts.tv_sec = 5;
    ts.tv_nsec = 0;

    while (m_bRun) {
        FD_ZERO(&fdsr);
        FD_SET(STDIN_FILENO, &fdsr);
        FD_SET(m_fdPipeKill[0], &fdsr);

        if (::pselect(STDIN_FILENO + 1, &fdsr, NULL, NULL, &ts, NULL) > 0) {
            if (FD_ISSET(STDIN_FILENO, &fdsr)) {
                std::getline(std::cin, strCmd);
                if (strCmd == "stop") {
                    m_bRun = false;
                }
                else if (strCmd == "wp") {
                    std::cerr << "!wp!" << std::endl;
                    m_bRun = false;
                    ::write(m_fdPipeKill[1], "1", strlen("1"));
                }
            }
        }
    }

    ::close(m_fdPipeKill[0]);
    ::close(m_fdPipeKill[1]);
}

/* MasterServer::WatcherTerminal
** Launch the threaded Terminal Watcher
*/
void MasterServer::watcherWebpanel(uint16_t _ui8Port) {
    linger sl { 1, 0 };
    SsocketOperations sockOpts(m_sckfdWP);
    sockOpts.socketCreate();
    sockOpts.optionsAdd({
        { SOL_SOCKET,	SO_REUSEADDR,	1  },
        { SOL_SOCKET,	SO_REUSEPORT,	1  },
        { IPPROTO_IPV6, IPV6_V6ONLY,	0  },
        { SOL_SOCKET,	SO_LINGER,		sl },
        { IPPROTO_TCP,	TCP_NODELAY,	1  }, // Disable Nagle's algorithm
        { IPPROTO_TCP,	TCP_CORK,	    0  }  // Disable Cork
        });
    sockOpts.socketBind(_ui8Port);

    // Create pipe for emergency stop
    if (::pipe2(m_fdPipeKill, O_NONBLOCK) == -1)
        SK_SHOWERROR(STRERROR);

    // Launch thread
    if (!m_thdWatcherWebpanel)
        m_thdWatcherWebpanel = new std::thread(&MasterServer::_watcherwebpanel, this);
}

/* MasterServer::_watcherwebpanel
** Monitors for a command input though the web panel
*/
void MasterServer::_watcherwebpanel() {
    SynakManager::signalBlockAll();

    // Accept web panel incoming connections
    if (::listen(m_sckfdWP, SOMAXCONN) != 0)
        SK_SHOWERROR(STRERROR);

    // Check incoming web panel instructions
    fd_set   fdsr;
    timespec ts;
    ts.tv_sec = 5;
    ts.tv_nsec = 0;
    int iMax { std::max(m_sckfdWP, m_fdPipeKill[0]) };

    while (m_bRun
        && m_sckfdWP != SOCKET_ERROR) {
        FD_ZERO(&fdsr);
        FD_SET(m_sckfdWP, &fdsr);
        FD_SET(m_fdPipeKill[0], &fdsr);

        if (::pselect(iMax + 1, &fdsr, NULL, NULL, &ts, NULL) > 0) {
            if (FD_ISSET(m_sckfdWP, &fdsr)
                && m_sckfdWP != SOCKET_ERROR) {
                in6_addr  addrRecv { 0 };
                socklen_t len { sizeof(addrRecv) };
                SOCKET m_sckfdNew = ::accept(m_sckfdWP, (sockaddr *)&addrRecv, &len);
                if (m_sckfdNew == SOCKET_ERROR)
                    SK_SHOWERROR(STRERROR);
                else {
                    char arrRecv[2048] { 0 };
                    if (::recv(m_sckfdNew, arrRecv, SK_ARRSIZE(arrRecv), MSG_NOSIGNAL) <= 0)
                        SK_SHOWERROR(STRERROR);
                    else {
                        json jRecv = json::parse(arrRecv);
                        std::cerr << arrRecv << std::endl;
                        if (!jRecv.is_null()) {
                            if (jRecv.contains("co_tpe")
                                && !jRecv["co_tpe"].empty()
                                && jRecv["co_tpe"].is_string())
                                std::cerr << "type: " << jRecv.at("co_tpe").get<std::string>() << std::endl;
                            if (jRecv.contains("co_act")
                                && !jRecv["co_act"].empty()
                                && jRecv["co_act"].is_number())
                                std::cerr << "action:" << jRecv.at("co_act").get<int>() << std::endl;
                        }

                        json jSend;
                        jSend["valid"] = true;
                        jSend["port"] = 12345;
                        std::string strJson { jSend.dump() };

                        if (::send(m_sckfdNew, strJson.c_str(), strJson.length(), MSG_NOSIGNAL) == -1)
                            SK_SHOWERROR(STRERROR);
                    }
                }

                SK_CLOSESOCKET(m_sckfdNew);
            }
        }
    }

    ::close(m_fdPipeKill[0]);
    ::close(m_fdPipeKill[1]);
}