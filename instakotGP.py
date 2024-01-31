try:
    from string import ascii_letters, digits
    from random import shuffle, choices
    from os import name as OSNAME
    from os import system, getpid
    from random import choice
    from sys import argv
    import subprocess
    import threading
    import json



    username = argv[1]
    filename = argv[2]
    method = argv[3]



    threads, timeout, rch = 150, 5, 0
    proxy_list, ExtraThreads = [], []
    fcb_add, CutOff, ProcessKilled, recieved = False, False, False, False
    Json = ''



    def Die():
        pid = getpid()
        if OSNAME == "nt":
            system(f"taskkill /F /PID {pid} > NUL")
        else:
            system(f"kill {pid} > /dev/null")



    def is_valid(ip_port):
        Dot = 0
        colon = 0
        valid_chars = list(digits+".:")

        for char in range(len(ip_port)):
            if ip_port[char] not in valid_chars:
                return "invalid_proxy"

            elif ip_port[char] == ':' or ip_port[char] == '.':
                if ip_port[char] == '.': Dot += 1
                elif ip_port[char] == ':': colon += 1
                try:
                    _ = int(ip_port[char+1])
                    _ = int(ip_port[char-1])
                except:
                    return "invalid_proxy"

        if Dot == 3 and colon != 1:
            return False
        elif Dot != 3 or colon != 1:
            return False
        else:
            return True



    def token():
        x_csrftoken = "".join(choices(ascii_letters + digits, k=32))
        x_asbd_id = "".join(choices(digits, k=6))
        return [x_csrftoken, x_asbd_id]



    def is_available(IpPort):
        global CutOff, ProcessKilled, recieved
        if CutOff == False:
            if method == "username":
                TOKENS = token()
                Command = [
                        "curl", "-i", "--http1.1", "-G",
                        "--connect-timeout", '3',
                        "--url", "https://www.instagram.com/api/v1/users/web_profile_info/?username="+username,
                        "--user-agent", "Mozilla/5.0 (Window`s NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
                        "-H", "Host: www.instagram.com",
                        "-H", "accept: */*",
                        "-H", "accept-language: en-US,en;q=0.9",
                        "-H", "sec-ch-prefers-color-scheme: dark",
                        "-H", "sec-fetch-dest: empty",
                        "-H", "sec-fetch-mode: cors",
                        "-H", "sec-fetch-site: same-origin",
                        "-H", f"x-csrftoken: {TOKENS[0]}",
                        "-H", f"x-asbd-id: {TOKENS[1]}",
                        "-H", "x-ig-app-id: 936619743392459",
                        "-H", "x-ig-www-claim: 0",
                        "-H", "x-requested-with: XMLHttpRequest",
                        "-H", f"Referer: https://www.instagram.com/{username}/",
                        "-H", "Referrer-Policy: strict-origin-when-cross-origin",
                        "--socks4", IpPort
                ]
            else:
                link = "https://www.instagram.com/graphql/query/"
                query_string = "query_hash=c9100bf9110dd6361671f113dd02e7d6"
                query_string_2 = "variables={%22user_id%22:%22"+username+"%22,%22include_chaining%22:false,%22include_reel%22:true,%22include_suggested_users%22:false,%22include_logged_out_extras%22:false,%22include_highlight_reels%22:false,%22include_related_profiles%22:false}"
                
                Command = [

                    "curl", "-i", "--http1.1", "-G",
                    "-d", query_string,
                    "-d", query_string_2,
                    "--url", link,
                    "--user-agent", "Mozilla/5.0 (Window`s NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
                    "-H", "Host: www.instagram.com",
                    "-H", "accept: */*",
                    "-H", "accept-language: en-US,en;q=0.9",
                    "--connect-timeout", '3'

                ]

            Respond = subprocess.run(Command, capture_output=True)
            Respond = (Respond.stderr + Respond.stdout).decode("utf-8")
            if "content-type: application/json" in Respond.lower() and "200 OK" in Respond:
                if recieved == False:
                    recieved, CutOff = True, True
                    with open(filename, "w+", encoding="utf-8") as user:
                        user.write(Respond)
                    user.close()
                    Die()
            elif "HTTP/1.1 404" in Respond:
                if recieved == False:
                    recieved, CutOff = True, True
                    with open(filename, "w+", encoding="utf-8") as user:
                        user.write("404 USER (the-computer-mayor)")
                    user.close()
                    Die()



    def cpl(IpsPorts):
        for IpPort in IpsPorts:
            if is_valid(IpPort) == True: is_available(IpPort)



    GetJson = subprocess.run([
        "curl", "--http1.1", "-i", 
        "--url", "https://raw.githubusercontent.com/the-computer-mayor/computer-mayor-db/main/PKPL.json",  
        "--connect-timeout", str(timeout),
        "--user-agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0", 
        "-H", f"Host: raw.githubusercontent.com",
        "-H", "Accept: */*"

    ], capture_output=True)
    GetJson = (GetJson.stderr + GetJson.stdout).decode("utf-8")



    for fcb in GetJson:
        if fcb in ['{', '}']:
            if fcb_add == False:
                fcb_add = True
            else:
                fcb_add = False
            Json += fcb
        elif fcb_add == True:
            Json += fcb

    PKPL = json.loads(Json)["socks4"]
    shuffle(PKPL)



    for link in PKPL:
        GetProxyList = subprocess.run(["curl", "--http1.1", link,  "-i", "--connect-timeout", str(timeout), "--user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0", "-H", "Accept: */*"], capture_output=True)
        GetProxyList = (GetProxyList.stderr + GetProxyList.stdout).decode("utf-8")
        if "200 OK" in GetProxyList:    
            proxy_list_uncleaned = GetProxyList.splitlines()
            fcb_add = False
            for pll in proxy_list_uncleaned[5:]:
                if pll == '':
                    fcb_add = True
                elif fcb_add == True:
                    proxy_list.append(pll)
            break



    p_calc = len(proxy_list) / threads
    while p_calc.is_integer() != True:
        Rproxy = choice(proxy_list)
        ExtraThreads.append(Rproxy)
        proxy_list.remove(Rproxy)
        p_calc = len(proxy_list) / threads
    origin_p_calc = int(p_calc)



    for making_thread in range(threads):
        INPUT_ARG = proxy_list[int(rch):int(p_calc)]
        T = threading.Thread(target=cpl, args=[INPUT_ARG])
        T.daemon = True
        rch = rch + origin_p_calc
        p_calc = p_calc + origin_p_calc
        T.start()
    for Extra_Thread in ExtraThreads:
        T = threading.Thread(target=cpl, args=[[Extra_Thread]])
        T.daemon = True
        T.start()
    while 1:None



except json.JSONDecodeError:
    print(False, end='')
