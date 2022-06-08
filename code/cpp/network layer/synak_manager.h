/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Network Layer
* synak_manager.h
*/

#pragma once

#include "network layer/synak.h"

namespace SK {
    /* struct SsocketOperations
    ** Struct for sockets operations (options, bind, etc)
    */
    struct SsocketOperations {
        /* SsocketOperations::Sopt
        ** Struct used to store socket options
        */
        struct Sopt {
            Sopt(int _iLevel, int _iOptName, socketoptval_t _aOptVal)
                : m_iLevel(_iLevel), m_iOptName(_iOptName), m_aOptVal(_aOptVal) {}

            int m_iLevel  { 0 },
                m_iOptName{ 0 };
            socketoptval_t m_aOptVal;
        };

        SsocketOperations(SOCKET &_ptrSockfd);
        bool optionsAdd(std::vector<Sopt> _vecOpts);
        bool socketCreate();
        bool socketBind(uint16_t _ui8Port, in6_addr _addr6in = IN6ADDR_ANY_INIT);

    private:
        SOCKET *m_ptrSockfd{ nullptr };
    };

    /* class SynakManager
    ** 
    */
    class SynakManager
    {
    public:
        ~SynakManager() {
            desinitialization();
        }

        void initialization();
        void desinitialization();

        static std::string strerror_sk() {
#ifdef _WIN32
            char cArrBuff[256] { '\0' };
            _strerror_s(cArrBuff, sizeof(cArrBuff), NULL);
            std::string strMess { std::string(cArrBuff) };
            return strMess;
#else
            return ::strerror(errno);
#endif
        }

    private:
    };
}