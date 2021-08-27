1. Change execution rights for the python files folder
chmod -R 0775 /var/www/synak/res/python

2. Create your password (/var/www/synak/.htpasswd)
openssl passwd -6 -salt <YOUR_SALT>

3. Add this line in your sudoers (visudo)
www-data ALL=(ALL) NOPASSWD: /var/www/synak/res/python/*.py

4. Need help with you DNS ZONE?
synak        3600 IN A     %IPV4%
synak        3600 IN AAAA  %IPV6%
www.synak    3600 IN CNAME synak.%DOMAIN%.%EXTENTION%.