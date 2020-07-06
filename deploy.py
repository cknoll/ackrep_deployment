"""
This script does the following:
- load specified settings
- find all templates (of config files)
- render these templates


for remote deployment

- stop remote services
- upload all files to the server
- restart remote services
"""

import sys
import os
import argparse
import yaml

sys.path.insert(0, "ackrep_core")

# noinspection PyUnresolvedReferences
from ackrep_core import core

from ipydex import IPS, activate_ips_on_exception
activate_ips_on_exception()

rendered_template_list = []


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("settingsfile", help=".yml-file for settings")

    args = argparser.parse_args()

    with open(args.settingsfile) as f:
        settings = yaml.load(f, Loader=yaml.FullLoader)

    res = find_and_render_templates(settings)
    rendered_template_list.extend(res)


def find_and_render_templates(settings_dict):

    # create a dict like {"template1.conf": {"value1": "abc", "value2": 10}, ...}
    template_settings_mapping = dict()

    for value in settings_dict.values():
        if not isinstance(value, dict):
            continue

        template = value.get("template")

        # load settings for this template
        ts_settings = value.get("settings")
        if template is not None:
            assert isinstance(ts_settings, dict)
            template_settings_mapping[template] = ts_settings

    # now render these templates
    results = []
    base_path = os.path.dirname(os.path.abspath(__file__))
    for template, settings in template_settings_mapping.items():
        context = dict(settings=settings)
        res = core.render_template(template, context=context, special_str=".template", base_path=base_path)
        results.append(res)

    return results



if __name__ == "__main__":
    main()