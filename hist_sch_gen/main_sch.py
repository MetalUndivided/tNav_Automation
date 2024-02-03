"""
Main script that generates historic schedule (timesteps, controls, wefacs, etc).
Refer to the supplied document for input data descripitions.
"""

import calendar
import sys

import pandas as pd
from tqdm import tqdm

from kwriter import *


def preprocess_prod(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the production history dataframe.

    :param df: dataframe containing production history
    :return: processed dataframe
    """

    df['DATE'] = pd.to_datetime(df['DATE'], format='%d.%m.%Y')

    df['month_length'] = df.apply(lambda row:
                                  calendar.monthrange(
                                      row['DATE'].year,
                                      row['DATE'].month
                                  )[1],
                                  axis=1)

    df['OIL'] = df['OIL'] / df['DAYS']
    df['WATER'] = df['WATER'] / df['DAYS']
    df['GAS'] = df['GAS'] / df['DAYS']
    df['WINJ'] = df['WINJ'] / df['DAYS']

    return df


def preprocess_perf(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the perforation data dataframe

    :param df: dataframe containing perforation data
    :return: processed dataframe
    """

    df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y')
    # rounding dates to simulation timesteps since data in csv doesn't align with timesteps
    df['Дата'] = df['Дата'].apply(lambda value:
                                  datetime.datetime(
                                      year=value.year,
                                      month=value.month,
                                      day=1
                                  )
                                  )

    df['perf_flag'] = df['Тип перфорации'].apply(lambda row:
                                                 True if pd.isna(row) else
                                                 True if 'ПЕРФ' in row else False
                                                 )

    return df


def preprocess_manops(df: pd.DataFrame) -> pd.DataFrame:

    df['Дата'] = pd.to_datetime(df['Дата'], format='%d.%m.%Y')

    return df


if __name__ == '__main__':

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    start_date = datetime.datetime.strptime(sys.argv[3], '%Y-%m-%d')
    end_date = datetime.datetime.strptime(sys.argv[4], '%Y-%m-%d')
    field = sys.argv[5]

    production = pd.read_csv(f'{input_directory}/production_kmb.csv', encoding='cp1251')
    production = pd.concat([production] +
                           [pd.read_csv(f'{input_directory}/production_tk.csv', encoding='cp1251')]
                           )
    production = production.merge(pd.read_csv(f'{input_directory}/well_table.csv', encoding='cp1251', sep=','),
                                  'left', left_on='*WELL', right_on='Название в модели')
    production = preprocess_prod(production)
    production = production[production['Привязка к залежи'] == field]
    
    perf = pd.read_csv(f'{input_directory}/perf_kmb_all.csv', encoding='cp1251', sep=';')
    perf = pd.concat([perf] +
                    [pd.read_csv(f'{input_directory}/perf_tk_all.csv', encoding='cp1251', sep=';')]
                    )
    perf = perf.drop_duplicates()
    perf = preprocess_perf(perf)
    perf = perf.merge(pd.read_csv(f'{input_directory}/well_table.csv', encoding='cp1251', sep=','),
                      'right', left_on='Скважина', right_on='Скважина в МЭР')
    perf = perf[perf['Привязка к залежи'] == field]

    perf_slice = perf[perf['Скважина'].isna()]
    assert perf_slice.shape[0] <= 1, f'Wells {list(perf_slice["Название в модели"])} have no perforations'

    man_ops = pd.read_csv(f'{input_directory}/man_ops.csv', encoding='cp1251')
    man_ops = preprocess_manops(man_ops)
    man_ops = man_ops[man_ops['Месторождение'] == field]

    first_month_flag = True  # prevents printing the first timestep DATES since it's defined in START kwd

    with open(f'{output_directory}/HIST.SCH', 'w') as outfile:
        for timestep in tqdm(pd.date_range(start_date, end_date, freq='1MS'), desc='writing timesteps'):

            if first_month_flag:  # perforations preceding the date specified in the START keyword
                perf_slice = perf[perf['Дата'] < timestep]
                for _, row in perf_slice.iterrows():
                    perf_out(
                        well_name=row['Название в модели'],
                        lower_depth=row['Глубина начала интервала перфорации(md), м'],
                        upper_depth=row['Глубина конца интервала перфорации(md), м'],
                        depth_type='MD',
                        status='OPEN' if row['perf_flag'] else 'SHUT',
                        well_diam=.16,
                        dest=outfile
                    )

            if not first_month_flag:

                dates_out(timestep.date(), dest=outfile)

                # resetting controls from previous timestep
                wconprodh_out('*', 'SHUT', 'LRAT', dest=outfile)
                wconinjh_out('*', 'WATER', 'SHUT', dest=outfile)
                wefac_out('*', 1, dest=outfile)

            first_month_flag = False

            production_slice = production[production['DATE'] == timestep]
            perf_slice = perf[perf['Дата'] == timestep]
            man_ops_slice = man_ops[man_ops['Дата'] == timestep]

            for _, row in perf_slice.iterrows():
                perf_out(
                    well_name=row['Название в модели'],
                    lower_depth=row['Глубина начала интервала перфорации(md), м'],
                    upper_depth=row['Глубина конца интервала перфорации(md), м'],
                    depth_type='MD',
                    status='OPEN' if row['perf_flag'] else 'SHUT',
                    well_diam=.16,
                    dest=outfile
                )

            # main controls
            for _, row in production_slice.iterrows():
                write_weff = False

                if row['WINJ'] > 0:
                    write_weff = True
                    wconinjh_out(
                        well_name=row['*WELL'],
                        injected_fluid='WATER',
                        well_status='OPEN',
                        inj_rate_h=row['WINJ'],
                        bhp_h=row['BHP'] if row['BHP'] > 0 else '*',
                        thp_h=row['THP'] if row['THP'] > 0 else '*',
                        well_control='RATE',
                        dest=outfile
                    )

                if row['OIL'] > 0:
                    write_weff = True
                    wconprodh_out(
                        well_name=row['*WELL'],
                        well_status='OPEN',
                        well_control='LRAT',
                        oil_rate_h=row['OIL'],
                        water_rate_h=row['WATER'],
                        gas_rate_h=row['GAS'],
                        thp_h=row['THP'] if row['THP'] > 0 else '*',
                        bhp_h=row['BHP'] if row['BHP'] > 0 else '*',
                        dest=outfile
                    )

                if write_weff:
                    wefac_out(
                        well_name=row['*WELL'],
                        efficiency_factor=row['DAYS'] / row['month_length'],
                        dest=outfile
                    )

            # manual operations
            for _, row in man_ops_slice.iterrows():

                generic_kw_out(
                    keyword=row['Ключевое слово'],
                    args=row['Аргумент'],
                    dest=outfile
                )
