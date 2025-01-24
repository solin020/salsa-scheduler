chown -R www-data /access-control/roles.txt
chmod +777 www-data /access-control/roles.txt
source /access-control/roles.txt
sed </etc/apache2/apache2base.conf "s/@{ADMINS}/${ADMINS}/" | sed "s/@{ANNOTATORS}/${ANNOTATORS}/" | sed "s/@{COORDINATORS}/${COORDINATORS}/"  | sed "s/,\+/,/" | sed "s/,}/}/" | sed "s/{,/{/"  > /etc/apache2/apache2.conf
apachectl start
shibd
while true 
do 
	inotifywait  -e close_write /access-control/roles.txt  
	source /access-control/roles.txt
       	sed </etc/apache2/apache2base.conf "s/@{ADMINS}/${ADMINS}/" | sed "s/@{ANNOTATORS}/${ANNOTATORS}/" | sed "s/@{COORDINATORS}/${COORDINATORS}/"  | sed "s/,\+/,/" | sed "s/,}/}/" | sed "s/{,/{/"  > /etc/apache2/apache2.conf
       	apachectl restart 
done