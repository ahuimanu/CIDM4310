# Connect Notebook to External Data

## Cases:

### Good: Access local CSV files
This allows you to just stick to what you learned from the Pandas Workshop.

### Good(er): Going the Google Sheets Route

#### The API way
We will rely on a 3rd Party Library for Python called [GSpread](https://docs.gspread.org/en/latest/index.html). You will need some things for setup:

* [Enable API Access for a Project](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access-for-a-project)
* [Enable Non-Human (Bot) Access Using a Service Account](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account)

#### The Shared Link Way
It is possible to just use sheet sharing as well: [Read Data from Google Sheets into Pandas without the Google Sheets API](https://towardsdatascience.com/read-data-from-google-sheets-into-pandas-without-the-google-sheets-api-5c468536550)

### Better: Going the Managed MySQL Route
We use the dashboard at Digital Ocean to perform all permissions and authorizations tasks

### Best: MySQL on VPS
The steps below will allow for external access to your VPS MySQL installation. All steps below assume you've complete BILC1.  
[Reference Article](https://www.digitalocean.com/community/tutorials/how-to-allow-remote-access-to-mysql):

1. Modify mysqld.cnf

```
lc-messages-dir = /usr/share/mysql
skip-external-locking
#
# Instead of skip-networking the default is now to listen only on
# localhost which is more compatible and is not less secure.
bind-address            = 0.0.0.0
```

2. Restart Server
   `sudo systemctl restart mysql`

3. Login as mysql user
   `sudo mysql`

4. Login to the MySQL server as root
   `mysql -u root -p`

5. Create an external user
   `CREATE USER 'sammy'@'remote_server_ip' IDENTIFIED BY 'password';` OR `CREATE USER 'sammy'@'remote_server_ip' IDENTIFIED WITH mysql_native_password BY 'password';`

6. Give the remote user priviliges
   `GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT, REFERENCES, RELOAD on *.* TO 'sammy'@'remote_server_ip' WITH GRANT OPTION;`

7. Refresh the Priviliges cache
   `FLUSH PRIVILEGES;`

8. Allow MySQL traffic through the firewall
   `sudo ufw allow from remote_IP_address to any port 3306`

9. try and verify remote access
   `mysql -u user -h database_server_ip -p`
