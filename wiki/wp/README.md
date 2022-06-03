# :bookmark_tabs: Web Panel README

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
2. Add the line ```www-data ALL=(ALL) NOPASSWD: /bin/tmux, /sbin/iptables, /sbin/ip6tables, /bin/ps, /bin/kill, /synak_ms/*, /var/www/synak/res/python/sk__req.cgi, /synak_ms/python/*, /synak_ms/db/blacklist_uid.db```
3. Press ```CTRL+X``` to close the file, then the ```Y``` key to save it, and finally the ```ENTER``` key to confirm

&#160;

## II. HTACCESS

### 1. PASSWORD CREATION
Generate your password to access to the Web Panel
1. In the terminal, type ```openssl passwd -6 -salt <YOUR_SALT>```
2. Obviously, you have to personalize ```<YOUR_SALT>```
3. Rename the [/var/www/synak/.htpasswd.SAMPLE](/var/www/synak/.htpasswd.SAMPLE) file into ```.htpasswd```
4. Edit it
    * Replace ```<SHA512>``` by your new generated key
    * Replace ```<USER>``` by a login name


### 2. IP PERMISSION
1. Rename [/var/www/synak/.htaccess.SAMPLE](/var/www/synak/.htaccess.SAMPLE) into ```.htaccess```
2. Edit it
    * [Line 14](/code/web/root/var/www/synak/.htaccess.SAMPLE#L14), add your IP by replacing ```<IP>```

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
1. Rename the [/code/web/root/synak_ms/wp_res/webpanel.permissions.SAMPLE](/code/web/root/synak_ms/wp_res/webpanel.permissions.SAMPLE) file to ```webpanel.permissions```
2. Edit it
    * Add any user with their corresponding rights (see the table below)

The **Web Panel** permissions file is a Json where each array corresponds to a new user and each element in that array is a granted right.

STRING FOR PERMISSIONS FILE | WHERE TO FIND IN THE WEB PANEL | PURPOSE
------------ | ------------- | -------------
**sk_mng_strt** | _MANAGING_ > _START_ | Starts the Master Server process
**sk_mng_stop** | _MANAGING_ > _STOP_ | Stops the Master Server process
**sk_mng_kill** | _MANAGING_ > _KILL_ | Kill the Master Server process
**sk_mng_optn** | _MANAGING_ > _OPTIONS_ | Change the configuration of the running Synak Master Server instance
**sk_mng_chck** | _MANAGING_ > _STATUS_ | Check if a Synak Master Server instance is running
**sk_mod_bani** | _MODERATION_ > _BAN_ | Ban IPv4, IPv6 or IPv4-mapped IPv6 addresses
**sk_mod_unbi** | _MODERATION_ > _UNBAN_ | Unban IPs addresses
**sk_mod_lsti** | _MODERATION_ > _LIST BANNED_ | List banned IPs
**sk_mod_banu** | _MODERATION_ > _BAN_ | Ban UIDs
**sk_mod_unbu** | _MODERATION_ > _UNBAN_ | Unban banned UIDs
**sk_mod_lstu** | _MODERATION_ > _LIST BANNED_ | List banned UIDs
**sk_mod_clnu** | _MODERATION_ > _CLEAR UP_ | Clean already passed bans
**sk_log_rtrv** | _LOG_ > _GET_ | Get log
**sk_log_eras** | _LOG_ > _ERASE_ | Erase log
**sk_nfo_cnfg** | _INFORMATION_ > _CONFIGURATION_ | Last configuration of the Synak Master Server
**sk_nfo_syms** | _INFORMATIONS_ > _MASTER SERVER_ | Get statistics from the Synak Master Server
**sk_nfo_dedi** | _INFORMATIONS_ > _DEDICATED SERVER_ | Get informations from the dedicated server
