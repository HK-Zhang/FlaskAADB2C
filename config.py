import os
import logging
from azure.keyvault.secrets import SecretClient
from azure.identity import ClientSecretCredential



# azure storage account setting
as_container_name = 'storagendtai'
as_blob_name = 'ndtai'
as_sas_token = '***stored in Valut***'
as_account_key = '***not permitted***'



appinsightKey = 'eedca9b9-6565-45ae-9850-2e8a58018312'
apiversion = '0.85'

AZURE_CLIENT_ID = "cd9f0f18-ee13-4327-b67b-7776c8ae8961"
AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
AZURE_TENANT_ID = "adf10e2b-b6e9-41d6-be2f-c12bb566019c"
KEY_VAULT_NAME = "kvNdtAiWewb"

global sas
sas = ""


def set_sas(val):
    global sas
    sas = val


def get_sas():
    global sas
    if sas == "":
        load_config()
    return sas


def load_config():
    credential = ClientSecretCredential(AZURE_TENANT_ID, AZURE_CLIENT_ID,
                                        AZURE_CLIENT_SECRET)
    KVUri = "https://" + KEY_VAULT_NAME + ".vault.azure.net"
    client = SecretClient(vault_url=KVUri, credential=credential)
    try:
        retrieved_secret = client.get_secret("blobSasToken")
        set_sas(retrieved_secret.value)
    except Exception:
        properties = {'custom_dimensions': {
        'error_code': 'app start', 'category': 'ai'}}
        logging.exception('Failed to read azure keyvault.', extra=properties)
