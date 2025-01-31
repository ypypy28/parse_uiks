﻿from selenium import webdriver

from pathlib import Path
from random import randrange
from re import findall
from selenium.common.exceptions import WebDriverException
from time import sleep
import sys

from parsix.config import SLEEP_RANGE


START_URL = 'http://www.ivanovo.vybory.izbirkom.ru/region/ivanovo?action=ik'


def get_src(url: str, show_chrome: bool) -> str:
    options = webdriver.chrome.options.Options()
    if not show_chrome:
        options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
    except WebDriverException as e:
        print("\nSomething happend while parsing:",
              url,
              "Maybe you were banned.",
              e.msg,
              sep='\n')
        driver.quit()
        sys.exit(1)


    arrows = driver.find_elements_by_class_name('jstree-ocl')[1:]
    for arrow in arrows:
        arrow.click()
        sleep(randrange(*SLEEP_RANGE))

    src = driver.page_source
    driver.quit()

    return src


def parse_ids(url: str = START_URL,
              out_dir: Path = None,
              show_chrome: bool = False) -> list:

    src = ''
    if out_dir is None:
        src = get_src(url, show_chrome)
    else:
        tmp = out_dir.joinpath("tmp_base.html")
        if tmp.is_file():
            src = tmp.read_text(encoding='utf-8')
        else:
            src = get_src(url, show_chrome)
            out_dir.joinpath("tmp_base.html").write_text(src, encoding='utf-8')

    return findall('id="(\d+)"', src)


if __name__ == '__main__':
    from time import (strftime, localtime)

    ids = parse_ids(START_URL)

    filename = (Path().cwd() / "out" /
                'uiks_' + strftime('%Y%m%d', localtime()) + '.txt'
                )

    with open(filename, 'w') as f:
        f.writelines((START_URL + f'%vrn={i}' for i in ids))
