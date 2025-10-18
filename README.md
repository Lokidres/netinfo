Local IP, Public IP ve Açık Port Gösterici

Bu Python scripti, kullanıcı flag’lerine göre kendi cihazınızın lokal IP’sini, public IP’sini ve dinleyen portlarını gösterir. Windows ve Unix tabanlı sistemler için uyumludur.

Gereksinimler

Python 3.x

(Opsiyonel) requests kütüphanesi, public IP almak için kullanılabilir.

pip install requests

Kullanım
python script.py [FLAGS]

Flag’ler

--local → Lokal IP adresinizi gösterir.

--public → Public IP adresinizi gösterir.

--ports → Cihazınızda dinleyen portları ve ilgili PID/proses bilgilerini listeler.

Örnekler

Sadece lokal IP:

python script.py --local


Public IP’yi göster:

python script.py --public


Tüm flag’leri kullan:

python script.py --local --public --ports

Çıktı Örneği
[destroyerr1558 Advanced Code Creator] İşletim Sistemi: Windows
[LOCAL IP BİLGİSİ]
Primary local IP: 192.168.1.10

[PUBLIC IP BİLGİSİ]
Public IP: 185.25.200.14

[AÇIK/DİNLEYEN PORTLAR]
TCP 0.0.0.0:135 PID=912 PROG=svchost.exe
TCP 0.0.0.0:445 PID=4 PROG=System
UDP 0.0.0.0:123 PID=988 PROG=svchost.exe

Notlar

Script yalnızca kendi cihazınızı tarar, başka cihazlara yönelik port taraması yapmaz.

Windows üzerinde port bilgisi netstat -ano ile, Unix tabanlı sistemlerde ss -tulnp veya netstat -tulnp ile alınır.

Public IP almak için çevrimiçi servislere erişim gereklidir.
