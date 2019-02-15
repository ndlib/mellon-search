#copy_pnx_to_Primo.sh 2/14/19 sm

# To make this executable, I had to do the following:
# Type the following command: sudo chmod +x *.sh

# move into the working directory containing PNX XML files
cd pnx

# create a separate tarball for every xml file in this directory
for f in *.xml ; do tar --disable-copyfile -zcf $f.tar.gz $f; done

# remove existing tar files from aleph before we copy our new files up
ssh -t -t smattiso@aleph1.library.nd.edu << 'RM'
rm *.tar.gz
exit
RM

#copy local tar files to aleph
scp *.tar.gz smattiso@aleph1.library.nd.edu:~

# remote into aleph to then copy files from aleph to the Primo sandbox
ssh -t -t smattiso@aleph1.library.nd.edu <<'ENDSSH'
scp -P 10022 *.tar.gz sftp_ndu@ndu-primo.hosted.exlibrisgroup.com:primodata/sandbox/snite_pnx
exit
ENDSSH

#return to original directory
cd ..

#save this for future reference to copy from aleph to the Primo sandbox
# copy all the files to the Primo Sandbox
#ssh sftp_ndu@ndu-primo.hosted.exlibrisgroup.com -p 10022
#scp -P 10022 *.tar.gz sftp_ndu@ndu-primo.hosted.exlibrisgroup.com:primodata/sandbox/snite_pnx
