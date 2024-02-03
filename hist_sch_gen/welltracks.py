"""
Generates WELLTRACKs.
Refer to the supplied document for input data specifications.
"""

import sys

import pandas as pd
from tqdm import tqdm

from kwriter import *

if __name__ == '__main__':

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    field = sys.argv[3]

    df = pd.read_csv(f'{input_directory}/traj_kmb_all.csv', sep=';')
    df = pd.concat([df] + [pd.read_csv(f'{input_directory}/traj_tk_all.csv', sep='\t')])

    # removes duplicates in case a well appears both in KMB and TK RN-KIN projects
    df['id_md'] = df['Скважина'].str.cat(df['MD'].astype('str'))
    df = df.drop_duplicates('id_md')

    df = df.merge(
        pd.read_csv(f'{input_directory}/well_table.csv', encoding='cp1251'),
        'right', left_on='Скважина', right_on='Скважина в МЭР'
    )

    df = df[df['Привязка к залежи'] == field]

    with open(f'{output_directory}/WELLTRACK.INC', 'w') as outfile:
        for well in tqdm(df['Название в модели'].unique(), desc='writing WELLTRACKS'):
            df_slice = df[df['Название в модели'] == well]

            assert df_slice['Скважина'].shape[0] > 1, f'Welltrack for well {well} is missing'

            specs_out(
                well_name=well,
                pad=df_slice.loc[df_slice.first_valid_index(), 'КП в модели'],
                dest=outfile)

            traj_out(
                well_name=well, coordinates=list(
                    df_slice[['Координата X', 'Координата Y', 'MD', 'Z']].itertuples(index=False, name=None)
                ),
                dest=outfile
            )
