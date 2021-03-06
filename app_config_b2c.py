import os

b2c_tenant = "dnvglb2cprod"
signupsignin_user_flow = "B2C_1A_SignInWithADFSIdp"
editprofile_user_flow = "b2c_1_edit_profile"
resetpassword_user_flow = "B2C_1_SSPR"
# authority_template = "https://login.microsoftonline.com/tfp/{tenant}.onmicrosoft.com/{user_flow}/v2.0"
authority_template = "https://{tenant}.b2clogin.com/{tenant}.onmicrosoft.com/{user_flow}"
CLIENT_ID = "7dc29f5a-2bc3-4da5-9613-f22cba33dd50"  # Application (client) ID of app registration

CLIENT_SECRET = os.environ.get('CLIENT_SECRET')  # Placeholder - for use ONLY during testing.
# In a production app, we recommend you use a more secure method of storing your secret,
# like Azure Key Vault. Or, use an environment variable as described in Flask's documentation:
# https://flask.palletsprojects.com/en/1.1.x/config/#configuring-from-environment-variables
# CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# if not CLIENT_SECRET:
#     raise ValueError("Need to define CLIENT_SECRET environment variable")

AUTHORITY = authority_template.format(tenant=b2c_tenant,
                                      user_flow=signupsignin_user_flow)
# B2C_PROFILE_AUTHORITY = authority_template.format(
#     tenant=b2c_tenant, user_flow=editprofile_user_flow)
# B2C_RESET_PASSWORD_AUTHORITY = authority_template.format(
#     tenant=b2c_tenant, user_flow=resetpassword_user_flow)

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.

# This is the API resource endpoint
ENDPOINT = 'https://localhost:5001'  # Application ID URI of app registration in Azure portal

# These are the scopes you've exposed in the web API app registration in the Azure portal
SCOPE = ["https://dnvglb2cprod.onmicrosoft.com/83054ebf-1d7b-43f5-82ad-b2bde84d7b75/user_impersonation"]  # Example with two exposed scopes: ["demo.read", "demo.write"]

SESSION_TYPE = "filesystem"  # Specifies the token cache should be stored in server-side session
