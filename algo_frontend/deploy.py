import os

os.system("yarn run build")
os.system("cd build && tar -czvf build.tar.gz *")
url = "satoshibot.tech"
os.system("scp build/build.tar.gz root@{}:/var/www/html/build.tar.gz".format(url))
os.system('ssh root@{} "cd /var/www/html/ && tar -xf build.tar.gz"'.format(url))
os.system('ssh root@{} "service apache2 restart"'.format(url))
