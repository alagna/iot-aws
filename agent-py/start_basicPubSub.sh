# stop script on error
set -e

# run pub/sub sample app using certificates downloaded in package
printf "\nRuning pub/sub sample application...\n"
python basicPubSub.py -e adttn6r67dmtu.iot.eu-west-1.amazonaws.com -r certificates/root-CA.crt -c certificates/rasp-felix001.cert.pem -k certificates/rasp-felix001.private.key
