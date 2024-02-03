"""
A library for writing tNav SCHEDULE keywords.
Refer to the respective function's docstrings for descriptions.
"""

import datetime
from typing import TextIO, Union, List


def _write_to_dest(
        string: str,
        dest: Union[str, TextIO]
        ) -> None:

    """
    Writes a string either to stdout or to the specified file.

    :param string: string to be written.
    :param dest: writing destination. Accepts either 'stdout' for writing to stdout
                 or a TextIO object for writing to files.
    :return: None
    """

    if dest == 'stdout':
        print(string)
    else:
        dest.writelines(string)


def specs_out(
        well_name: str,
        pad: str = None,
        coord_x: float = None,
        coord_y: float = None,
        ref_depth: float = None,
        phase: str = 'LIQ',
        drainage_radius: float = None,
        special_inflow: str = None,
        eco_behavior: str = None,
        crossflow_flag: str = None,
        pres_table_num: int = None,
        dens_calc_type: str = None,
        fip_region: int = None,
        dest: Union[str, TextIO] = 'stdout'
        ) -> None:
    """
    Writes WELSPECS tNav keyword to the specified destination.
    Please refer to the tNav documentation for argument descriptions.

    :param well_name: arg 1 of tNav WELSPECS keyword
    :param pad: arg 2 of tNav WELSPECS keyword
    :param coord_x: arg 3 of tNav WELSPECS keyword
    :param coord_y: arg 4 of tNav WELSPECS keyword
    :param ref_depth: arg 5 of tNav WELSPECS keyword
    :param phase: arg 6 of tNav WELSPECS keyword
    :param drainage_radius: arg 7 of tNav WELSPECS keyword
    :param special_inflow: arg 8 of tNav WELSPECS keyword
    :param eco_behavior: arg 9 of tNav WELSPECS keyword
    :param crossflow_flag: arg 10 of tNav WELSPECS keyword
    :param pres_table_num: arg 11 of tNav WELSPECS keyword
    :param dens_calc_type: arg 12 of tNav WELSPECS keyword
    :param fip_region: arg 13 of tNav WELSPECS keyword
    :param dest: writing destination. Accepts either 'stdout' for writing to stdout
                 or a TextIO object for writing to files.
    :return: None
    """

    input_args = locals()
    input_args.pop('dest')

    keyword = 'WELSPECS\n'

    for keyword_arg in input_args.items():
        arg, val = keyword_arg
        keyword += (str(val) if val is not None else '*') + ' '
    keyword += '/\n'
    keyword += '/\n\n'

    _write_to_dest(keyword, dest)


def traj_out(
        well_name: str,
        coordinates: List[tuple],
        dest: Union[str, TextIO] = 'stdout'
        ) -> None:

    """
    Writes WELLTRACK tNav keyword to the specified destination, single-branch mode.
    Please refer to the tNav documentation for argument descriptions.

    :param well_name: well name
    :param coordinates: a list of tuples containing all the well trajectory points. Each tuple is a trajectory point.
                        Tuple structure must be the following:
                            [0] - X coordinate;
                            [1] - Y coordinate;
                            [2] - MD;
                            [3] - Z coordinate;
    :param dest: writing destination. Accepts either 'stdout' for writing to stdout
                 or a TextIO object for writing to files.
    :return: None
    """

    keyword = f'WELLTRACK {well_name}\n'

    for coord_point in coordinates:
        coord_x, coord_y, md, coord_z = coord_point
        keyword += f'{coord_x} {coord_y} {coord_z} {md} \n'

    keyword += '/\n\n'

    _write_to_dest(keyword, dest)


def dates_out(
        timestamp: Union[datetime.datetime, datetime.date],
        dest: Union[str, TextIO] = 'stdout'
) -> None:
    """
    Writes DATES tNav keyword to the specified output.
    Please refer to the tNav documentation for argument descriptions.

    :param timestamp: a datetime.datetime or datetime.date object.
                      Passing a date object will suppress writing of hours, minutes and seconds.
                      Otherwise, if passed a datetime object, the hours, minutes and seconds will always be written.
    :param dest: writing destination. Accepts either 'stdout' for writing to stdout
                 or a TextIO object for writing to files.
    :return: None
    """

    month_codes = {
        1: 'JAN',
        2: 'FEB',
        3: 'MAR',
        4: 'APR',
        5: 'MAY',
        6: 'JUN',
        7: 'JLY',
        8: 'AUG',
        9: 'SEP',
        10: 'OCT',
        11: 'NOV',
        12: 'DEC'
    }

    day = timestamp.day
    month = month_codes[timestamp.month]
    year = timestamp.year
    try:
        hour = timestamp.hour
        minute = timestamp.minute
        second = timestamp.second
    except AttributeError:
        hour, minute, second = None, None, None

    hour_tail = '' if hour is None else f'{hour:02}:{minute:02}:{second:02} '

    keyword = 'DATES\n'
    keyword += f'{day:02} {month} {year} {hour_tail}/\n'
    keyword += '/\n\n'

    _write_to_dest(keyword, dest)


def wconprodh_out(
        well_name: str,
        well_status: str = 'SHUT',
        well_control: str = 'LRAT',
        oil_rate_h: float = None,
        water_rate_h: float = None,
        gas_rate_h: float = None,
        vfp_num: int = None,
        alq: float = None,
        thp_h: float = None,
        bhp_h: float = None,
        wet_gas_rate_h: float = None,
        ngl_rate_h: float = None,
        dest: Union[str, TextIO] = 'stdout'
) -> None:
    """
    Writes WCONHIST tNav keyword to the specified output.
    Please refer to the tNav documentation for argument descriptions.

    :param well_name: arg 1 of tNav WCONHIST keyword
    :param well_status: arg 2 of tNav WCONHIST keyword
    :param well_control: arg 3 of tNav WCONHIST keyword
    :param oil_rate_h: arg 4 of tNav WCONHIST keyword
    :param water_rate_h: arg 5 of tNav WCONHIST keyword
    :param gas_rate_h: arg 6 of tNav WCONHIST keyword
    :param vfp_num: arg 7 of tNav WCONHIST keyword
    :param alq: arg 8 of tNav WCONHIST keyword
    :param thp_h: arg 9 of tNav WCONHIST keyword
    :param bhp_h: arg 10 of tNav WCONHIST keyword
    :param wet_gas_rate_h: arg 11 of tNav WCONHIST keyword
    :param ngl_rate_h: arg 12 of tNav WCONHIST keyword
    :param dest: writing destination. Accepts either 'stdout' for writing to stdout
                 or a TextIO object for writing to files.
    :return: None
    """

    initial_args = locals()
    initial_args.pop('dest')

    keyword = 'WCONHIST\n'
    for keyword_arg in initial_args.items():
        arg, val = keyword_arg

        keyword += '* ' if val is None else f'{str(val)} '

    keyword += '/\n'
    keyword += '/\n\n'

    _write_to_dest(keyword, dest)


def wconinjh_out(
        well_name: str,
        injected_fluid: str = 'WATER',
        well_status: str = 'SHUT',
        inj_rate_h: float = None,
        bhp_h: float = None,
        thp_h: float = None,
        vfp_num: int = None,
        second_phase_concentration: float = None,
        surf_oil_part: float = None,
        surf_water_part: float = None,
        surf_gas_part: float = None,
        well_control: str = 'RATE',
        dest: Union[str, TextIO] = 'stdout'
) -> None:
    """
    Writes WCONINJH tNav keyword to the specified output.
    Please refer to the tNav documentation for argument descriptions.

    :param well_name: arg 1 of tNav WCONINJH keyword
    :param injected_fluid: arg 2 of tNav WCONINJH keyword
    :param well_status: arg 3 of tNav WCONINJH keyword
    :param inj_rate_h: arg 4 of tNav WCONINJH keyword
    :param bhp_h: arg 5 of tNav WCONINJH keyword
    :param thp_h: arg 6 of tNav WCONINJH keyword
    :param vfp_num: arg 7 of tNav WCONINJH keyword
    :param second_phase_concentration: arg 8 of tNav WCONINJH keyword
    :param surf_oil_part: arg 9 of tNav WCONINJH keyword
    :param surf_water_part: arg 10 of tNav WCONINJH keyword
    :param surf_gas_part: arg 11 of tNav WCONINJH keyword
    :param well_control: arg 12 of tNav WCONINJH keyword
    :param dest: writing destination. Accepts either 'stdout' for writing to stdout
                 or a TextIO object for writing to files.
    :return:
    """

    initial_args = locals()
    initial_args.pop('dest')

    keyword = 'WCONINJH\n'
    for keyword_arg in initial_args.items():
        arg, val = keyword_arg

        keyword += '* ' if val is None else f'{str(val)} '

    keyword += '/\n'
    keyword += '/\n\n'

    _write_to_dest(keyword, dest)


def wefac_out(
        well_name: str,
        efficiency_factor: float = 1,
        apply_to_network: str = None,
        dest: Union[str, TextIO] = 'stdout'
) -> None:
    """
    Writes WEFAC tNav keyword to the specified output.
    Please refer to the tNav documentation for argument descriptions.

    :param well_name: arg 1 of tNav WEFAC keyword
    :param efficiency_factor: arg 2 of tNav WEFAC keyword
    :param apply_to_network: arg 3 of tNav WEFAC keyword
    :param dest: writing destination. Accepts either 'stdout' for writing to stdout
                 or a TextIO object for writing to files.
    :return: None
    """

    initial_args = locals()
    initial_args.pop('dest')

    keyword = 'WEFAC\n'
    for keyword_arg in initial_args.items():
        arg, val = keyword_arg

        keyword += '* ' if val is None else f'{str(val)} '

    keyword += '/\n'
    keyword += '/\n\n'

    _write_to_dest(keyword, dest)


def perf_out(
        well_name: str,
        branch_num: int = None,
        lower_depth: float = None,
        upper_depth: float = None,
        depth_type: str = None,
        status: str = None,
        sat_num: int = None,
        trans_factor: float = None,
        well_diam: float = None,
        effective_kh: float = None,
        skin: float = 0,
        d_factor: float = None,
        connection_factor_mult: float = 1,
        completion_type: str = None,
        dest: Union[str, TextIO] = 'stdout'
) -> None:
    """
    Writes COMPDATMD tNav keyword to the specified output.
    Please refer to the tNav documentation for argument descriptions.

    :param well_name: arg 1 of tNav COMPDATMD keyword
    :param branch_num: arg 2 of tNav COMPDATMD keyword
    :param lower_depth: arg 3 of tNav COMPDATMD keyword
    :param upper_depth: arg 4 of tNav COMPDATMD keyword
    :param depth_type: arg 5 of tNav COMPDATMD keyword
    :param status: arg 6 of tNav COMPDATMD keyword
    :param sat_num: arg 7 of tNav COMPDATMD keyword
    :param trans_factor: arg 8 of tNav COMPDATMD keyword
    :param well_diam: arg 9 of tNav COMPDATMD keyword
    :param effective_kh: arg 10 of tNav COMPDATMD keyword
    :param skin: arg 11 of tNav COMPDATMD keyword
    :param d_factor: arg 12 of tNav COMPDATMD keyword
    :param connection_factor_mult: arg 13 of tNav COMPDATMD keyword
    :param completion_type: arg 14 of tNav COMPDATMD keyword
    :param dest: writing destination. Accepts either 'stdout' for writing to stdout
                 or a TextIO object for writing to files.
    :return: None
    """

    initial_args = locals()
    initial_args.pop('dest')

    keyword = 'COMPDATMD\n'
    for keyword_arg in initial_args.items():
        arg, val = keyword_arg

        keyword += '* ' if val is None else f'{str(val)} '

    keyword += '/\n'
    keyword += '/\n\n'

    _write_to_dest(keyword, dest)


def generic_kw_out(
        keyword: str,
        args: str,
        dest: Union[str, TextIO] = 'stdout'
        ) -> None:

    """
    Writes a generic tNav keyword to the specified destination.
    Keyword arguments must be supplied as a string according to the keyword specifications (refer to tNav documentation).

    :param keyword: keyword to be written
    :param args: keyword arguments as a string (e.g. well_name OPEN 10 * /)
    :param dest: writing destination. Accepts either 'stdout' for writing to stdout
                 or a TextIO object for writing to files.
    :return: None
    """

    keyword += '\n'
    keyword += args + '\n/\n\n'

    _write_to_dest(keyword, dest)
