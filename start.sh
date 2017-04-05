# stop script on error
set -e

# run pub/sub sample app using certificates downloaded in package
printf "\nRuning pub/sub sample application...\n"
python basicPubSub.py -e adttn6r67dmtu.iot.eu-west-1.amazonaws.com -r certs/root-CA.crt -c certs/mypi.cert.pem -k certs/mypi.private.key
