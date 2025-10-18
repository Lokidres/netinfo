import argparse,platform,subprocess,re,socket

def detect_os():
    return platform.system()

def get_primary_ip():
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        ip=s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

def parse_windows_netstat(out):
    lines=[l.strip() for l in out.splitlines() if l.strip()]
    results=[]
    for l in lines:
        if re.search(r'\bLISTENING\b',l):
            parts=re.split(r'\s+',l)
            if len(parts)>=5:
                proto=parts[0]
                local=parts[1]
                state=parts[3] if proto.upper()=="TCP" else ""
                pid=parts[-1]
                host,port=local.rsplit(":",1) if ":" in local else (local,"")
                results.append((proto,host,port,pid))
    return results

def get_windows_process_name(pid):
    try:
        out=subprocess.check_output(["tasklist","/FI",f"PID eq {pid}"],encoding="utf-8",errors="ignore")
        lines=out.splitlines()
        if len(lines)>=4:
            entry=re.split(r'\s{2,}',lines[3].strip())
            return entry[0] if entry else ""
    except:
        pass
    return ""

def parse_unix_ss(out):
    lines=[l for l in out.splitlines() if l.strip() and not l.startswith("State")]
    results=[]
    for l in lines:
        cols=re.split(r'\s+',l,6)
        if len(cols)>=6:
            state=cols[0]
            local=cols[4]
            proc=cols[5] if len(cols)>=6 else ""
            if state.upper().startswith("LISTEN"):
                if local.startswith("[") and "]:" in local:
                    host,port = re.match(r'(\[.*?\]):(\d+)',local).groups()
                else:
                    host,port=local.rsplit(":",1) if ":" in local else (local,"")
                pid_match=re.search(r'pid=(\d+)',proc)
                pid=pid_match.group(1) if pid_match else ""
                proc_name_match=re.search(r'\"?([^\",()]+)',proc)
                proc_name=proc_name_match.group(1) if proc_name_match else ""
                results.append(("tcp/udp",host,port,pid,proc_name))
    return results

def get_public_ip():
    services=["https://api.ipify.org","https://ifconfig.me/ip","https://icanhazip.com"]
    try:
        import requests
    except:
        requests=None
    for svc in services:
        try:
            if requests:
                r=requests.get(svc,timeout=3)
                if r.ok: return r.text.strip()
            else:
                from urllib.request import urlopen
                with urlopen(svc,timeout=4) as resp:
                    data=resp.read().decode().strip()
                    if data: return data
        except:
            continue
    return None

def run(args):
    osn=detect_os()
    print("[destroyerr1558 Advanced Code Creator] İşletim Sistemi:",osn)
    if args.local:
        ip=get_primary_ip()
        print("\n[LOCAL IP BİLGİSİ]")
        print("Primary local IP:",ip if ip else "Bulunamadı")
    if args.public:
        pub=get_public_ip()
        print("\n[PUBLIC IP BİLGİSİ]")
        print("Public IP:",pub if pub else "Bulunamadı")
    if args.ports:
        print("\n[AÇIK/DİNLEYEN PORTLAR]")
        if osn=="Windows":
            try:
                out=subprocess.check_output(["netstat","-ano"],encoding="utf-8",errors="ignore")
            except:
                out=""
            parsed=parse_windows_netstat(out)
            for proto,host,port,pid in parsed:
                pname=get_windows_process_name(pid)
                print(f"{proto} {host}:{port} PID={pid} PROG={pname}")
        else:
            try:
                out=subprocess.check_output(["ss","-tulnp"],encoding="utf-8",errors="ignore")
            except:
                try:
                    out=subprocess.check_output(["netstat","-tulnp"],encoding="utf-8",errors="ignore")
                except:
                    out=""
            parsed=parse_unix_ss(out)
            for proto,host,port,pid,proc in parsed:
                print(f"{proto} {host}:{port} PID={pid} PROG={proc}")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--local",action="store_true")
    parser.add_argument("--public",action="store_true")
    parser.add_argument("--ports",action="store_true")
    args=parser.parse_args()
    if not (args.local or args.public or args.ports):
        parser.error("En az bir flag belirtmelisiniz: --local, --public veya --ports")
    run(args)
