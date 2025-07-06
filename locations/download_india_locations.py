import pandas as pd
import requests
import zipfile
import io
import os

# Download Geonames all India places (cities/villages/towns)
GEONAMES_URL = 'https://download.geonames.org/export/dump/IN.zip'
OUTPUT_CSV = 'india_locations.csv'

print('Downloading India location data from Geonames...')
r = requests.get(GEONAMES_URL)
z = zipfile.ZipFile(io.BytesIO(r.content))
with z.open('IN.txt') as f:
    # Geonames columns: https://download.geonames.org/export/dump/readme.txt
    cols = [
        'geonameid','name','asciiname','alternatenames','latitude','longitude','feature class','feature code',
        'country code','cc2','admin1 code','admin2 code','admin3 code','admin4 code','population','elevation',
        'dem','timezone','modification date'
    ]
    df = pd.read_csv(f, sep='\t', names=cols, dtype=str, low_memory=False)

# Map admin1 code to state name
admin1_url = 'https://download.geonames.org/export/dump/admin1CodesASCII.txt'
admin1_df = pd.read_csv(admin1_url, sep='\t', names=['code','state','asciiname','geonameid'], dtype=str)
admin1_df['state_code'] = admin1_df['code'].str.split('.', expand=True)[1]
admin1_map = dict(zip(admin1_df['state_code'], admin1_df['state']))

df['state'] = df['admin1 code'].map(admin1_map)

# Map admin2 code to district name (not always perfect, but best available)
admin2_url = 'https://download.geonames.org/export/dump/admin2Codes.txt'
admin2_df = pd.read_csv(admin2_url, sep='\t', names=['code','district','asciiname','geonameid'], dtype=str)
admin2_df['state_code'] = admin2_df['code'].str.split('.', expand=True)[1]
admin2_df['district_code'] = admin2_df['code'].str.split('.', expand=True)[2]
admin2_map = dict(zip(admin2_df['code'], admin2_df['district']))
df['admin2_full'] = 'IN.' + df['admin1 code'].fillna('') + '.' + df['admin2 code'].fillna('')
df['district'] = df['admin2_full'].map(admin2_map)

# Only keep rows with state and district
df = df[df['state'].notnull() & df['district'].notnull()]

# Output columns: state, district, city_village
out_df = df[['state','district','name']].rename(columns={'name':'city_village'})

# Remove duplicates
out_df = out_df.drop_duplicates()

# Save to CSV
output_dir = os.path.dirname(OUTPUT_CSV)
if output_dir:
    os.makedirs(output_dir, exist_ok=True)
out_df.to_csv(OUTPUT_CSV, index=False)
print(f'Saved {len(out_df)} locations to {OUTPUT_CSV}') 