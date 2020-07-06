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
import deploymentutils as du

from ipydex import IPS, activate_ips_on_exception
activate_ips_on_exception()

mod_path = os.path.dirname(os.path.abspath(__file__))
core_mod_path = os.path.join(mod_path, "..", "ackrep_core")
sys.path.insert(0, core_mod_path)
from ackrep_core import core


rendered_template_list = []


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("settingsfile", help=".yml-file for settings")
    argparser.add_argument("-nd", "--no-docker", help="omit docker comands", action="store_true")

    args = argparser.parse_args()

    with open(args.settingsfile) as f:
        settings = yaml.load(f, Loader=yaml.FullLoader)

    # ------------------------------------------------------------------------------------------------------------------
    print("find and render templates")
    res = find_and_render_templates(settings)
    rendered_template_list.extend(res)

    if settings["type"] == "local":
        print(du.bgreen("done"))
        exit(0)

    local_deployment_files_base_dir = du.get_dir_of_this_file()
    general_base_dir = os.path.split(local_deployment_files_base_dir)[0]

    c = du.StateConnection(settings["url"], user=settings["user"], target=settings["type"])

    # ------------------------------------------------------------------------------------------------------------------
    print("stop running services (this might fail in the first run)")

    # we do not use os.path.join here because the target platform is unix but the host platform should be flexible
    remote_deployment_path = f"{settings['target_path']}/ackrep_deployment"
    c.chdir(remote_deployment_path)
    c.run(f"docker-compose down", target_spec="remote", printonly=args.no_docker)

    # ------------------------------------------------------------------------------------------------------------------
    print("upload all deployment files")
    source_path = general_base_dir+os.path.sep
    c.rsync_upload(source_path, settings["target_path"], target_spec="remote", printonly=False)

    # ------------------------------------------------------------------------------------------------------------------
    print("restart the services")
    remote_deployment_path = f"{settings['target_path']}/ackrep_deployment"
    c.chdir(remote_deployment_path)
    c.run(f"docker-compose up -d", target_spec="remote", printonly=args.no_docker)


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
    base_path = mod_path

    for template, settings in template_settings_mapping.items():
        context = dict(settings=settings)
        res = core.render_template(template, context=context, special_str=".template", base_path=base_path)
        results.append(res)

    return results


if __name__ == "__main__":
    main()
