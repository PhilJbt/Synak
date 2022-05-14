/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server
* synak_masterserver.h
*/

#pragma once

#include "master server/synak_masterserver_define.h"


namespace SK {
    /* class SynakManager
    **
    */
    class MasterServer {
        friend std::thread;

    public:
        /* General
        **
        */
        void initialization(int _argc, char *_argv[]);
        void desinitialization();

        static void epollAdd(epoll_event *_ev, const int &_epfd, int _fd, int _iAction, bool _bAssign = false, int _iFlags = 0);

        static volatile std::atomic_bool m_bRun;


        /* Web Panel watcher
        **
        */
        void WP_watcherTerminal_Launch();
        void WP_watcherWebPanel_Launch(int _iPort);
        static void WP_signalBlockAllExcept(int _iFlags = 0);
        static void WP_signalHandler(int _signum);
        int WP_port() { return m_WP_iPort; }

        SOCKET m_WP_sckfd = SOCKET_ERROR;
        static int m_WP_fdPipeKill[2];


        /* Log writing
        **
        */
        enum class eLogType : int {
            NFO,
            ATT,
            ERR
        };
        template<typename... Args>
        static void LW_writeLog(std::string _strFileLine, eLogType _eType, Args&& ... args);
        static void LW_flushLog();

        static int  m_LW_iLogID;

    private:
        /* General
        **
        */
        void configBackup();

        int m_IG_iPort = 45350;


        /* Web Panel watcher
        **
        */
        void WP_watcherTerminal_thd();
        void WP_watcherWebPanel_tdh();

        std::thread *m_WP_thdWatcherTerminal = nullptr,
                    *m_WP_thdWatcherWebpanel = nullptr;

        int m_WP_iPort = 45318;


        /* Log writing
        **
        */
        static std::string LW_writeLog_toStr(int _iVal);
        static std::string LW_writeLog_toStr(std::string _str);
        static std::string LW_writeLog_toStr(const char *_cz);
        static std::string LW_cleanLine(std::string _str);

        static eLogType m_LW_eLogLevel;
    };

    /* // MS CLIENTS SOCKET
    SOL_SOCKET, SO_KEEPALIVE, 1
    IPPROTO_TCP, TCP_KEEPIDLE, 1
    IPPROTO_TCP, TCP_KEEPINTVL, 2
    IPPROTO_TCP, TCP_KEEPCNT, 15
    SOL_SOCKET, SO_RCVBUF, 212990
    SOL_SOCKET, SO_SNDBUF, 212990
    */

    /*

    int epfd = ::epoll_create(2);
    if(epfd == -1)
        SK_LOG_ERR(STRERROR);

    epoll_event ev[2];
    ev[0].events = EPOLLIN | EPOLLRDHUP | EPOLLERR;
    ev[0].data.fd = STDIN_FILENO;
    if(::epoll_ctl(epfd, EPOLL_CTL_ADD, STDIN_FILENO, &ev[0]) != 0)
        SK_LOG_ERR(STRERROR);

    ev[1].events = EPOLLIN | EPOLLRDHUP | EPOLLERR;
    ev[1].data.fd = m_WP_fdPipeKill[0];
    if(::epoll_ctl(epfd, EPOLL_CTL_ADD, m_WP_fdPipeKill[0], &ev[0]) != 0)
        SK_LOG_ERR(STRERROR);

    while(m_bRun) {
        int nfds = ::epoll_wait(epfd, ev, 10, 5000);
        if (nfds < 0)
            SK_LOG_ERR(STRERROR);
        else {
            for(int i = 0; i < nfds; ++i) {
                if(ev[i].data.fd == STDIN_FILENO
                    && ev[i].events & EPOLLIN) {
                    std::getline(std::cin, strCmd);
                    if(strCmd == "stop") {
                        m_bRun = false;
                        ::write(m_WP_fdPipeKill[1], "1", strlen("1"));
                    }
                }
            }
        }
    }

    if(::epoll_ctl(epfd, EPOLL_CTL_DEL, STDIN_FILENO, &ev[0]) == -1)
        SK_LOG_ERR(STRERROR);

    if(::epoll_ctl(epfd, EPOLL_CTL_DEL, m_WP_fdPipeKill[0], &ev[1]) == -1)
        SK_LOG_ERR(STRERROR);

    */
}

#define NoExtraWarning_SK_MS_TEMPLATE
#include "synak_masterserver_writelog_template.cpp" NoExtraWarning_SK_MS_TEMPLATE
