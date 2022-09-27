import subprocess, time

FILE_NAME_BASE_CA = 'ela-ca'
CN = "ElliottArnold-CA"

def gen_certificate_auth_pk():
    return f'openssl genrsa -out {FILE_NAME_BASE_CA}.key 2048'


def gen_certificate_signing_request():
    return f'openssl req -new -key {FILE_NAME_BASE_CA}.key -subj "/CN={CN}" -out {FILE_NAME_BASE_CA}.csr'
   

def sign_certificate():
    return f"openssl x509 -req -in {FILE_NAME_BASE_CA}.csr -signkey {FILE_NAME_BASE_CA}.key -days 10000 -CAcreateserial -extensions v3_ext  -out {FILE_NAME_BASE_CA}.crt"

def verify_csr():
    return f'openssl req -text -in {FILE_NAME_BASE_CA}.csr -noout -verify'


def sign_certificate():
    return f"openssl x509 -req -in {FILE_NAME_BASE_CA}.csr -signkey {FILE_NAME_BASE_CA}.key -out {FILE_NAME_BASE_CA}.crt"

def run_cmd(cmd):
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    time.sleep(8)


def gen_self_signed_cert():
    ca_steps = [gen_certificate_auth_pk(), gen_certificate_signing_request(), verify_csr(), sign_certificate()]
    [run_cmd(cmd) for cmd in ca_steps]


if __name__ == "__main__":
    gen_self_signed_cert()


#create key pair  (public and private)
#create certificate signing request (csr)

# https://www.ibm.com/support/pages/openssl-commands-check-and-verify-your-ssl-certificate-key-and-csr
# https://kubernetes.io/docs/tasks/administer-cluster/certificates/


#  openssl req -x509 -new -nodes -key ca.key -subj "/CN=k8s" -days 10000 -out ca.crt
#   575  openssl genrsa -out server.key 2048
#   576  openssl req -new -key server.key -subj "/CN=elliott" -out server.csr
#   577  openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key     -CAcreateserial -out server.crt -days 10000     -extensions v3_ext
#   578  openssl req  -noout -text -in ./server.csr
#   579  openssl x509  -noout -text -in ./server.crt


# openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
#     -CAcreateserial -out server.crt -days 10000 -extensions v3_ext

# openssl req -x509 -new -nodes -key ca.key -subj "/CN=eliottca" -days 10000 -out ca.crt
# openssl req -new -key server.key -out server.csr -subj "/CN=eliottadmin"

# curl https://192.168.49.2:8443/api/v1/pods --key "./server.key" --cert "./server.crt" --cacert "./ca.crt"