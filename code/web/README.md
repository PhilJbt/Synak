# Web Panel README

&#160;

## I. FOLDER PERMISSIONS

### 1. PYTHON FOLDER PERMISSIONS
Change execution rights for the python files folder
1. In the terminal, type ```chmod -R 0775 /var/www/synak/res/python```

### 2. MASTER SERVER BINARY PERMISSIONS
Change execution rights for the **Master Server binary**
1. In the terminal, type ```chmod 0775 /synak_ms/synak_ms.bin```

### 3. USER WWW-DATA PERMISSIONS
The ```WWW-DATA``` user needs permissions to execute python scripts
1. In the terminal, type ```visudo```
2. Add the line ```www-data ALL=(ALL) NOPASSWD: /bin/tmux, /sbin/iptables, /sbin/ip6tables, /bin/ps, /bin/kill, /synak_ms/*, /var/www/synak/res/python/*.py```
3. Press ```CTRL+X``` to close the file, then the ```Y``` key to save it, and finally the ```ENTER``` key to confirm

&#160;

## II. HTACCESS

### 1. PASSWORD CREATION
Generate your password to access to the Web Panel
1. In the terminal, type ```openssl passwd -6 -salt <YOUR_SALT>```
2. Obviously, you have to personalize ```<YOUR_SALT>```
3. Rename the [/var/www/synak/.htpasswd.SAMPLE](root/var/www/synak/.htpasswd.SAMPLE) file into ```.htpasswd```
4. Edit it
    * Replace ```<SHA512>``` by your new generated key
    * Replace ```<USER>``` by a login name


### 2. IP PERMISSION
1. Rename [/var/www/synak/.htaccess.SAMPLE](root/var/www/synak/.htaccess.SAMPLE) into ```.htaccess```
2. Edit it
    * [Line 14](root/var/www/synak/.htaccess.SAMPLE#L14), add your IP by replacing ```<IP>```

To add a new IP, add a new ```Allow from``` line (IPv4 and IPv6 are supported).
    
&#160;

## III. ZONE DNS
In case you are lost with you dns zone, here three useful lines (the ending dot is **NOT** a mistake)
````
synak        3600 IN A     <IPV4>
synak        3600 IN AAAA  <IPV6>
www.synak    3600 IN CNAME synak.<DOMAIN>.<EXTENTION>.
````
Replace ```<IPV4>```, ```IPV6``` and ```<DOMAIN>.<EXTENTION>``` by yours.

&#160;

## IV. USER PERMISSIONS
In case you want to provide an access to the **Web Panel** to multiple individuals, give them different permissions may be necessary.\
Disabled by default, create the permissions file will enable it.
1. Rename the [/var/www/synak/res/webpanel.permissions.SAMPLE](root/var/www/synak/res/webpanel.permissions.SAMPLE) file to ```webpanel.permissions```
2. Edit it
    * Add any user with their corresponding rights (see the table below)

The **Web Panel** permissions file is a Json where each array corresponds to a new user and each element in that array is a granted right.

STRING FOR PERMISSIONS FILE | WHERE TO FIND IN THE WEB PANEL | PURPOSE
------------ | ------------- | -------------
**sk_mng_srt** | _MANAGING_ > _START_ | Starts the Master Server process
**sk_mng_stp** | _MANAGING_ > _STOP_ | Stops the Master Server process
**sk_mng_kll** | _MANAGING_ > _KILL_ | Kill the Master Server process
**sk_mod_ban** | _MODERATION_ > _BAN_ | Ban an IPv4, IPv6 or IPv4-mapped IPv6 address
**sk_mod_unb** | _MODERATION_ > _UNBAN_ | See and unban banned IPs
**sk_log_get** | _LOG_ > _GET_ | Get logs
**sk_nfo_sms** | _INFORMATIONS_ > _MASTER SERVER_ | Get statistics from the Synak Master Server
**sk_nfo_ded** | _INFORMATIONS_ > _DEDICATED SERVER_ | Get informations from the dedicated server
