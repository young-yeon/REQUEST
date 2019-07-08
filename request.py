"""
=============================================================
Implement http protocol and https protocol using tcp protocol
=============================================================
Writer : young-yeon
Date   : (UTC +9) 2019.07.08 PM 10:02
=============================================================
"""

import socket
from abc import ABCMeta, abstractmethod


class Request(metaclass = ABCMeta):

    def __init__(self, url):
        # Default Settings

        self.url = url
        self.err = "[*] Deleted."
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if type(self.url) is not type("str"):
            self.err = "[*] Input is not of String type"
            del self
        if "http://" in self.url:
            self.port = 80
            self.url = self.url[7:]
        elif "https://" in self.url:
            self.port = 443
            self.url = self.url[8:]
        else:
            self.err = "[*] Please check to see if there is a protocol in URL."
            del self


    @abstractmethod
    def get(self):
        pass


    @abstractmethod
    def post(self):
        pass


    def __del__(self):
        print(self.err)



class Http_request(Request):

    def get(self, cookie = {}, data = {}):
        # GET method in http protocol
        # Check params

        param = self.url[self.url.find("/")+1:]
        host = self.url[:self.url.find("/")]
        try:
            if param[-1] != "?":
                param += "?"
            for key in data.keys():
                param += key + "=" + data[key] + "&"
            param = param[:len(param)-1]
        except IndexError:
            pass
        except:
            self.err = "[*] Unexcepted Error."
            del self
        
        # Check cookies

        try:
            coo = ""
            for key in cookie.keys():
                coo += key + "=" + cookie[key] + ";"
            coo = coo[:len(coo)-1]
            if param[-1] == "/":
                param = param[:len(param)-1]
        except IndexError:
            pass
        except:
            self.err = "[*] Unexcepted Error."
            del self

        # Requesting and receiving response from HOST

        try:
            req = "GET /%s HTTP/1.1\nHost: %s\nCookie: %s\n\n" \
                %(param, host, coo)
            self.sock.connect((host, self.port))
            self.sock.sendall(req.encode())
            buff = b""
            buff_size = 8192
            while True:
                part = self.sock.recv(buff_size)
                buff += part
                if len(part) < buff_size:
                    break
            self.sock.close()
            response = buff.decode()
            if "302 Moved Temporarily" in response:
                self.err = "[*] Please check if its protocol is 'https' or moved site."
                del self
            return buff.decode()
        except:
            self.err = "[*] Fail to connect."
            del self
            exit(0)


    def post(self):
        pass



class Https_request(Request):

    def get(self):
        pass
    
    def post(self):
        pass



if __name__ == "__main__":

    print()
    
    # webhacking.kr <- Normal response : 200

    print("=" * 61)
    print("TestA : http://webhacking.kr/index.php?mode=challenge")
    print("=" * 61)
    print("\n")

    testA = Http_request("http://webhacking.kr/index.php")
    data = {"mode":"challenge"}
    cookie = {"PHPSESSID":"ef30fe68f0cd334992fd001050cb5164"}
    print(testA.get(data=data,cookie=cookie))

    print("\n" * 3)

    # www.naver.com <- A site that uses the https protocol : 302

    print("=" * 61)
    print("TestB : http://www.naver.com/")
    print("=" * 61)
    print("\n")
    
    testB = Http_request("http://www.naver.com/")
    print(testB.get())


