/* SYNAK NETWORK LIBRARY - Philippe Jaubert
* https://github.com/PhilJbt/Synak/
* Master Server's log writer template
* synak_masterserver_writelog_template.cpp
*/


/* MasterServer::LW_writeLog
** Write messages in log file
*/
template<typename... Args>
void SK::MasterServer::LW_writeLog(std::string _strFileLine, eLogType _eType, Args&& ... args) {
    if (static_cast<int>(_eType) < static_cast<int>(SK::MasterServer::m_LW_eLogLevel))
        return;
    
    std::string strMess( "[" );
    ((strMess += "\"" + LW_cleanLine(LW_writeLog_toStr(args)) + "\","), ...);
    strMess[strMess.length() - 1] = ']';

    std::string strTime(20, 0);
    std::time_t t = std::time(nullptr);
    strTime.resize(std::strftime(&strTime[0], strTime.size(), "%H:%M:%S %d/%m/%Y", std::localtime(&t)));

    std::string strLogType;
    switch (static_cast<int>(_eType)) {
        case 0:  strLogType = "NFO"; break;
        case 1:  strLogType = "ATT"; break;
        case 2:  strLogType = "ERR"; break;
        default: strLogType = "N/A"; break;
    }

    std::ios_base::openmode iosOpenmode(std::ios_base::binary | std::ios_base::out | std::ios_base::app);
    std::string strPath("/synak_ms/synak_ms.log"),
    strLine (
        "[\"" + std::to_string(++m_LW_iLogID) + "\","
        "\"" + strLogType + "\","
        "\"" + _strFileLine + "\","
        "\"" + strTime + "\","
        + strMess + "]"
    );
    std::ofstream fLogFile(strPath, iosOpenmode);
    
    if(fLogFile) {
        fLogFile << strLine << std::endl;
        if(!fLogFile.bad()) {
            fLogFile.close();
            std::cout.flush();
        }
    }
}
