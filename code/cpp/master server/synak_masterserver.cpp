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
void SK::MasterServer::initialization() {
    m_bRun = true;

    WP_signalBlockAllExcept();

    struct sigaction sigbreak;
    ::sigemptyset(&sigbreak.sa_mask);
    sigbreak.sa_handler = &MasterServer::WP_signalHandler;
    sigbreak.sa_flags = 0;
    if (::sigaction(SIGUSR1, &sigbreak, NULL) != 0)
        SK_WRITELOG(SK_FILENLINE, "ERR", STRERROR);
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
