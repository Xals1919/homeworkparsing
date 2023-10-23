from pprint import pprint
import json
import code



if __name__ == '__main__':
    URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
    os='Windows'
    browser='Chrome'
    create_json = code.Save_json(URL, os, browser)
    result_save = create_json.save_js()
    result_open = create_json.open_js()
    pprint(result_open)