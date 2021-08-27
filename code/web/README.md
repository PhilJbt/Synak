## I. PYTHON FOLDER PERMISSIONS
Change execution rights for the python files folder
1. In the terminal, type ```chmod -R 0775 /var/www/synak/res/python```

&#160;

## II. USER WWW-DATA PERMISSIONS
The WWW-DATA user needs permissions to execute python scripts
1. In the terminal, type ```visudo```
2. Add the line ```www-data ALL=(ALL) NOPASSWD: /var/www/synak/res/python/*.py```

&#160;

## III. PASSWORD CREATION (.HTACCESS)
Create your password to access to the Web Panel
1. In the terminal, type ```openssl passwd -6 -salt <YOUR_SALT>```
2. Then /var/www/synak/.htpasswd

&#160;

## VI. ZONE DNS
In case you are lost with you dns zone, here three useful lines

    *```synak        3600 IN A     %IPV4%```
    * ```synak        3600 IN AAAA  %IPV6%```
    * ```www.synak    3600 IN CNAME synak.%DOMAIN%.%EXTENTION%.``` (the ending dot is **NOT** a mistake)
