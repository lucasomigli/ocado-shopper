from selenium.common.exceptions import NoSuchElementException
import json


def exists(webdriver, validator, type):
    if type == 'xpath':
        try:
            webdriver.find_element_by_xpath(validator)

        except NoSuchElementException:
            return False

        return True

    elif type == 'class':
        try:
            webdriver.find_element_by_class_name(validator)

        except NoSuchElementException:
            return False

        return True

    elif type == 'css':
        try:
            webdriver.find_element_by_class_css(validator)

        except NoSuchElementException:
            return False

        return True


def set_arguments(argParser):
    with open('grocery.json', 'r+') as f:
        groceries = json.load(f)

        for item in groceries:
            argParser.add_argument(
                '--{}'.format(item),
                default=1,
                help='set number of {} (default: 1)'.format(item))

    return argParser.parse_args()