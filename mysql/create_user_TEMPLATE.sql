USE mysql;
CREATE USER "$MYSQL_USER$"@"localhost" IDENTIFIED BY "";
GRANT ALL PRIVILEGES ON *.* TO "$MYSQL_USER$"@"localhost";
UPDATE user SET plugin="mysql_native_password" WHERE User="%MYSQL_USER$";
FLUSH PRIVILEGES;
exit;
