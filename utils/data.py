import pandas as pd
import os
from shareplum import Site
from shareplum import Office365
from shareplum.site import Version

def load_data(admin=False):
    # use_sharepoint = os.getenv("USE_SHAREPOINT", "false") == "true"
    
    # if use_sharepoint:
    #     # Connexion SharePoint
    #     from utils.sharepoint import download_excel_from_sharepoint
    #     file = download_excel_from_sharepoint()
    #     df = pd.read_excel(file, sheet_name="Suivi-des-activités")
    # else:
    df = pd.read_excel("Suivi-des-activités 2025.xlsx")
        #, sheet_name="Suivi-des-activités")
    
    # if not admin:
    #     user = os.getenv("USER_CONNECTED", "").lower()
    #     df = df[df["Responsable"].str.lower() == user]
    
    return df

