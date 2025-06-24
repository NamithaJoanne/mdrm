# mdrm_script.py

import requests
import zipfile
import os
from datetime import datetime
import pandas as pd

def run_mdrm_script():
    output_dir = 'output_' + datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created folder: {output_dir}")

    zip_path = os.path.join(output_dir, 'mdrm.zip')
    url = 'https://www.federalreserve.gov/apps/mdrm/pdf/MDRM.zip'
    response = requests.get(url)
    response.raise_for_status()
    with open(zip_path, 'wb') as f:
        f.write(response.content)

    extract_dir = os.path.join(output_dir, 'mdrm_data')
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

    csv_path = os.path.join(extract_dir, 'MDRM_CSV.csv')
    df = pd.read_csv(csv_path, header=1)
    df.columns = df.columns.str.strip()
    df['End Date'] = df['End Date'].astype(str).str.strip()
    df['Reporting Form'] = df['Reporting Form'].astype(str).str.replace("", "")
    df['MDRM_Name'] = df['Reporting Form'] + ':' + df['Mnemonic'] + df['Item Code']
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    df_with_9999 = df[df['End Date'].str.contains("9999", na=False)]
    df_without_9999 = df[~df['End Date'].str.contains("9999", na=False)]

    df_with_9999.to_csv(os.path.join(output_dir, 'end_date_9999.csv'), index=False)
    df_without_9999.to_csv(os.path.join(output_dir, 'end_date_not_9999.csv'), index=False)

    print(f"Done! Files saved to: {output_dir}")
    return output_dir
