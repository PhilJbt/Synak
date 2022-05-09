/* MasterServer::writeLog
** Write messages in log file
*/
template<typename... Args>
void SK::MasterServer::writeLog(std::string _strFileLine, std::string _strType, Args&& ... args) {
    
    std::string strMess { "[" };
    ((strMess += "\"" + _writeLog_toStr(args) + "\","), ...);
    strMess[strMess.length() - 1] = ']';

    std::string strTime(20, 0);
    std::time_t t = std::time(nullptr);
    strTime.resize(std::strftime(&strTime[0], strTime.size(),
        "%H:%M:%S %d/%m/%Y", std::localtime(&t)));

    std::ios_base::openmode iosOpenmode { std::ios_base::binary | std::ios_base::out | (m_bLogTruncate ? std::ios_base::trunc : std::ios_base::app) };
    std::string strPath { "/synak_ms/synak_ms.log" },
    strLine {
        "[\"" + std::to_string(++m_iLogID) + "\","
        "\"" + _strType + "\","
        "\"" + _strFileLine + "\","
        "\"" + strTime + "\","
        + strMess + "]"
    };
    std::ofstream fLogFile(strPath, iosOpenmode);
    
    if(fLogFile) {
        fLogFile << strLine << std::endl;
        if(fLogFile.bad())
            std::cerr << "Can't write the log file (file permissions?): " << STRERROR << std::endl;
        else {
            fLogFile.close();
            std::cout.flush();
        }
    }
    else
        std::cerr << "Can't open/create the log file (file permissions?): " << STRERROR << std::endl;
}
