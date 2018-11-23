@echo off

echo Nahravam %1

:: Pripravim FTP settings
echo open                                                     > settings.ftp
more FTPaddress                                              >> settings.ftp
more FTPusername                                             >> settings.ftp
more FTPpassword                                             >> settings.ftp
echo lcd D:\GitHub\OSM-Garmin-Maps-by-VasaM\img              >> settings.ftp
echo cd  maps/                                               >> settings.ftp
echo binary                                                  >> settings.ftp
echo put %1_VasaM.info                                       >> settings.ftp

echo ! rename %1_VasaM.img           %1_VasaM.img.uploading  >> settings.ftp
echo   put    %1_VasaM.img.uploading                         >> settings.ftp
echo   rename %1_VasaM.img.uploading %1_VasaM.img            >> settings.ftp
echo ! rename %1_VasaM.img.uploading %1_VasaM.img            >> settings.ftp

echo ! rename %1_VasaM.zip           %1_VasaM.zip.uploading  >> settings.ftp
echo   put    %1_VasaM.zip.uploading                         >> settings.ftp
echo   rename %1_VasaM.zip.uploading %1_VasaM.zip            >> settings.ftp
echo ! rename %1_VasaM.zip.uploading %1_VasaM.zip            >> settings.ftp

echo disconnect                                              >> settings.ftp
echo quit                                                    >> settings.ftp

ftp -s:settings.ftp

del settings.ftp
