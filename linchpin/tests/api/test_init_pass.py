import os

from nose.tools import *

import logging
from unittest import TestCase

try:
    import configparser as ConfigParser
except ImportError:
    import ConfigParser as ConfigParser

from linchpin.api import LinchpinAPI
from linchpin.api.context import LinchpinContext
from linchpin.tests.mockdata.contextdata import ContextData


def test_api_create():

    lpc = LinchpinContext()
    lpc.load_config()
    lpa = LinchpinAPI(lpc)

    assert_equal(isinstance(lpa, LinchpinAPI), True)


def setup_load_config():

    """
    Perform setup of ContextData() object, and run get_temp_filename()
    """

    global cd
    global provider
    global config_path
    global config_data

    provider = 'dummy'

    cd = ContextData()
    cd.load_config_data(provider)
    cd.parse_config()
    config_path = cd.get_temp_filename()
    config_data = cd.cfg_data
    cd.write_config_file(config_path)


def setup_lp_api():

    """
    Perform setup of LinchpinContext, lpc.load_config, and LinchPinAPI
    """

    global lpc
    global lpa

    global target
    global pinfile

    base_path = '{0}'.format(os.path.dirname(
        os.path.realpath(__file__))).rstrip('/')
    lib_path = os.path.realpath(os.path.join(base_path, os.pardir))

    setup_load_config()

    pinfile = 'PinFile'
    mock_path = '{0}/{1}/{2}'.format(lib_path, 'mockdata', provider)

    lpc = LinchpinContext()
    lpc.load_config(lpconfig=config_path)
    lpc.load_global_evars()
    lpc.setup_logging()
    lpc.workspace = os.path.realpath(mock_path)

    lpa = LinchpinAPI(lpc)


@with_setup(setup_lp_api)
def test_set_cfg():

    test_dict = {'key': 'value', 'key2': 'value2'}

    for k, v in test_dict.items():
        lpa.set_cfg('test', k, v)

    assert_dict_equal(test_dict, lpa.ctx.cfgs.get('test'))


@with_setup(setup_lp_api)
def test_get_cfg_section():

    lpa.set_cfg('test', 'key', 'value')
    lpa_dict = lpa.get_cfg('test')

    assert_dict_equal(lpa_dict, lpa.ctx.cfgs.get('test'))


@with_setup(setup_lp_api)
def test_get_cfg_item():

    lpa.set_cfg('test', 'key', 'value')
    lpa_value = lpa.get_cfg('test', 'key')

    test_dict = lpa.ctx.cfgs.get('test')
    test_value = test_dict.get('key')

    assert_equal(lpa_value, test_value)


@with_setup(setup_lp_api)
def test_set_evar():

    test_evars = {'ekey': 'evalue'}

    for k, v in test_evars.items():
        lpa.set_evar(k, v)
    lpa_evars = lpa.get_cfg('evars')

    assert_dict_contains_subset(test_evars, lpa_evars)


@with_setup(setup_lp_api)
def test_get_all_evars():

    test_evars = {'ekey1': 'evalue1', 'ekey2': 'evalue2'}
    for k, v in test_evars.items():
        lpa.set_evar(k, v)

    lpa_evars = lpa.get_evar()

    assert_dict_contains_subset(test_evars, lpa_evars)


@with_setup(setup_lp_api)
def test_get_evar_item():

    test_evars = {'ekey2': 'evalue2'}
    for k, v in test_evars.items():
        lpa.set_evar(k, v)

    assert_equal(lpa.get_evar(key='ekey2'), test_evars.get('ekey2'))


#def setup_lp_api():
#
#    """
#    Perform setup of LinchpinContext, lpc.load_config, and LinchPinAPI
#    """
#
#    global lpc
#    global lpa
#
#    lpc = LinchpinContext()
#    lpc.load_config()
#    lpa = LinchpinAPI(lpc)

@with_setup(setup_lp_api)
def test_run_playbook():

    pf_w_path = '{0}/{1}'.format(lpc.workspace, pinfile)
    results = lpa.run_playbook(pf_w_path, targets=[provider])

    for res in results[provider]:
        name = res._task.get_name()
        failed = False
        if res.is_failed():
            failed = True

    assert not failed


def main():

    pass

if __name__ == '__main__':
    sys.exit(main())
