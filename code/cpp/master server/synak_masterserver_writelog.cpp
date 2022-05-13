/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server's log writer
* synak_masterserver_writelog.cpp
*/

#include "master server/synak_masterserver.h"


int SK::MasterServer::m_LW_iLogID = 0;


/* SK::MasterServer::LW_writeLog_toStr(T _rval)
** Function needed for fold expression, int specialisation
*/
std::string SK::MasterServer::LW_writeLog_toStr(int _iVal) {
    return std::to_string(_iVal);
}

/* SK::MasterServer::LW_writeLog_toStr(std::string _str)
** Function needed for fold expression, std::string specialisation
*/
std::string SK::MasterServer::LW_writeLog_toStr(std::string _str) {
    return _str;
}

/* SK::MasterServer::LW_writeLog_toStr(const char *_cz)
** Function needed for fold expression, char pointer specialisation
*/
std::string SK::MasterServer::LW_writeLog_toStr(const char *_cz) {
    return std::string(_cz);
}

/* SK::MasterServer::LW_writeLog_toStr(const char *_cz)
** Function escaping apostrophes, quotation marks, square brackets, slashes and back slashes.
*/
std::string SK::MasterServer::LW_cleanLine(std::string _str) {
    std::string strLine;

    for (unsigned int i(0); i < _str.length(); ++i) {
        switch (_str[i]) {
        default:
            strLine += _str[i];
            break;
        case '\\':
            strLine += "&#92;";
            break;
        case '/':
            strLine += "&#47;";
            break;
        case '"':
            strLine += "&#34;";
            break;
        case '\'':
            strLine += "&#39;";
            break;
        case '[':
            strLine += "&#91;";
            break;
        case ']':
            strLine += "&#93;";
            break;
        case '{':
            strLine += "&#123;";
            break;
        case '}':
            strLine += "&#125;";
            break;
        }
    }

    return strLine;
}

/* MasterServer::LW_flushLog
** Flush log file
*/
void SK::MasterServer::LW_flushLog() {
    std::ios_base::openmode iosOpenmode(std::ios_base::binary | std::ios_base::out | std::ios_base::trunc);
    std::string strPath("/synak_ms/synak_ms.log");
    std::ofstream fLogFile(strPath, iosOpenmode);

    if (fLogFile) {
        if (fLogFile.bad())
            std::cerr << "Can't write the log file (file permissions?): " << STRERROR << std::endl;
        else {
            fLogFile.close();
            std::cout.flush();
        }
    }
    else
        std::cerr << "Can't open/create the log file (file permissions?): " << STRERROR << std::endl;
}