#include "synak.h"

void SynakManager::Launch() {
	SOCKET sockfd;

#ifdef _WIN32
	WSADATA wsa;

	if (::WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
		return;

	if ((sockfd = ::socket(AF_INET6, SOCK_STREAM, IPPROTO_IP)) == INVALID_SOCKET)
		::printf("Could not create socket : %d\n", ::WSAGetLastError());
#else
	if ((sockfd = ::socket(AF_INET6, SOCK_STREAM, 0)) == SOCKET_ERROR)
		::printf("Could not create socket : %d\n", ::strerror(errno));

	int yes { 1 },
		no  { 0 };
	if (::setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR,  (void*)&yes, sizeof(yes)) != 0)
		::printf("SO_REUSEADDR : %s\n", ::strerror(errno));
	if (::setsockopt(sockfd, IPPROTO_IPV6, IPV6_V6ONLY, (void*)&no, sizeof(no)) != 0)
		::printf("IPV6_V6ONLY : %s\n", ::strerror(errno));

	sockaddr_in6 addrAccept;
	::memset(&addrAccept, 0, sizeof(addrAccept));
	addrAccept.sin6_addr = IN6ADDR_ANY_INIT;
    addrAccept.sin6_port = htons(45318);
    addrAccept.sin6_family = AF_INET6;
	if (::bind(sockfd, (sockaddr*)&addrAccept, INET6_ADDRSTRLEN) == SOCKET_ERROR)
		::printf("bind : %s\n", ::strerror(errno));

	int res = ::listen(sockfd, SOMAXCONN);
	if (res == 0) {
		in6_addr addrRecv = { 0 };
		socklen_t len = sizeof(addrRecv);
		SOCKET newClient = ::accept(sockfd, (sockaddr*)&addrRecv, &len);
		if (newClient == SOCKET_ERROR)
			::printf("accept : %s\n", ::strerror(errno));
		else {
            char arrRecv[2048]{ 0 };
			if (::recv(newClient, arrRecv, SK_ARRSIZE(arrRecv), 0) <= 0)
				::printf("recv : %s\n", ::strerror(errno));
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
				std::string strJson{ jSend.dump() };

				if (::send(newClient, strJson.c_str(), strJson.length(), 0) == -1)
					::printf("send : %s\n", ::strerror(errno));
			}
		}
		::shutdown(newClient, SHUT_RDWR);
		closesocket(newClient);
	}
	else
		::printf("listen : %s\n", ::strerror(errno));

	::shutdown(sockfd, SHUT_RDWR);
	closesocket(sockfd);
#endif

#ifdef _WIN32
	WSACleanup();
#endif
}