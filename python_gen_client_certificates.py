from python_gen_cert_auth import FILE_NAME_BASE_CA
import subprocess, time

FILE_NAME_BASE_ADMIN = 'ela-k8s-admin'
CN = 'elliott-k8s-admin'


def gen_certificate_auth_pk():
    return f'openssl genrsa -out {FILE_NAME_BASE_ADMIN}.key 2048'

def gen_certificate_signing_request():
    return f'openssl req -new -key {FILE_NAME_BASE_ADMIN}.key -subj "/CN={CN}" -out {FILE_NAME_BASE_ADMIN}.csr'

def sign_usr_certificate():
    return f"openssl x509 -req -in {FILE_NAME_BASE_ADMIN}.csr -CA {FILE_NAME_BASE_CA}.crt -CAkey {FILE_NAME_BASE_CA}.key -days 10000 -CAcreateserial -extensions v3_ext  -out {FILE_NAME_BASE_ADMIN}.crt"

def run_cmd(cmd):
    subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    time.sleep(8)


def gen_admin_cert():
    ca_steps = [gen_certificate_auth_pk(),gen_certificate_signing_request(), sign_usr_certificate()]
    [run_cmd(cmd) for cmd in ca_steps]


gen_admin_cert()



# https://www.ibm.com/support/pages/openssl-commands-check-and-verify-your-ssl-certificate-key-and-csr

#  curl https://127.0.0.1:59532/api/v1/pods --key ela-k8s-admin.key --cert ela-k8s-admin.crt --cacert ela-ca.crt --insecure


# curl https://192.168.49.2:8443/api/v1/pods --key "./ela-k8s-admin.key" --cert "./ela-k8s-admin.crt" --cacert "./ela-ca.crt" --insecure

# kubectl config view | grep http
#   553  history | grep kube


# openssl x509 -req -in {FILE_NAME_BASE_ADMIN}.csr -CA {FILE_NAME_BASE_CA}.crt -CAkey {FILE_NAME_BASE_CA}.key -out {FILE_NAME_BASE_ADMIN}.crt