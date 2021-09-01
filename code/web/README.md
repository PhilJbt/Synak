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
2. Add the line ```www-data ALL=(ALL) NOPASSWD: /bin/ps, /bin/kill, /synak_ms/synak_ms.bin, /var/www/synak/res/python/*.py```

&#160;

## II. HTACCESS

### 1. PASSWORD CREATION
Generate your password to access to the Web Panel
1. In the terminal, type ```openssl passwd -6 -salt <YOUR_SALT>```
2. Obviously, you have to personalize ```<YOUR_SALT>```
3. In [/var/www/synak/.htpasswd.SAMPLE](root/var/www/synak/.htpasswd.SAMPLE#L1), replace ```<SHA512>``` by your new generated key
3. In [/var/www/synak/.htpasswd.SAMPLE](root/var/www/synak/.htpasswd.SAMPLE#L1), replace ```<USER>``` by your login name
4. Rename [/var/www/synak/.htaccess.SAMPLE](root/var/www/synak/.htaccess.SAMPLE) into ```.htaccess```
5. Rename [/var/www/synak/.htpasswd.SAMPLE](root/var/www/synak/.htpasswd.SAMPLE) into ```.htpasswd```

### 2. IP PERMISSION
Go to the line 14 of the [/var/www/synak/.htaccess](root/var/www/synak/.htaccess#L14) file and add your IP by replacing ```<IP>```.\
To add a new IP, add a new ```Allow from``` line (IPv4 and IPv6 are supported).
    
&#160;

## III. ZONE DNS
In case you are lost with you dns zone, here three useful lines (the ending dot is **NOT** a mistake)

    synak        3600 IN A     <IPV4>
    synak        3600 IN AAAA  <IPV6>
    www.synak    3600 IN CNAME synak.<DOMAIN>.<EXTENTION>.
