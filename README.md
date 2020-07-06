# ACKRep Deployment Utis

## General Information

This repository contains the code that runs on <demo.ackrep.org>. It should also provide a starting point to deploy an own instance.

## Deployment concept

The ackrep project consists of several components which are maintained each in their own repository.


**Functional Components**

- *ackrep_core*
    - main code of the ackrep engine and command-line-interface (cli)
- *ackrep_data*
    - actual data for the repository
- (*ackrep_web*)
    - code for the web front-end
    - currently still part of ackrep_core

**Auxiliary Components**

- *ackrep_deployment*
    - code for simple deployment of the functional components on a virtual server
- *custom_settings*
    - data used for customization and maintainance. For privacy and security reasons these settings are not published.


These components are represented by the following **directory layout**:

    <ackrep_project_dir>/                 ← deployment code for the ackrep project
    ├── ackrep_deployment/                 ← deployment code for the ackrep project
    │  ├── .git/
    │  ├── README.md                      ← the currently displayed file (README.md)
    │  ├── deploy.py                      ← deployment script
    │  ├── ...
    │  ├── ackrep_data/                      ← symbolic link to ../ackrep_data (relative path)
    │  ├── ackrep_core/                      ← symbolic link to ../ackrep_core (relative path)
    │  ├── ...
    │  ├── custom_settings__demo          ← instance-specific settings
    │  │   ├── settings.yml
    │  │   └── ...
    │  ├── custom_settings__local         ← settings for local testing deployment
    │  │   ├── settings.yml
    │  │   └── ...
    │  └── template_custom_settings       ← template/example for the custom settings
    │      ├── settings.yml
    │      └── ...
    │
    ├── ackrep_data/                      ← actual repository for ackrep_data
    │  ├── .git/
    │  └── ...
    └── ackrep_core/                      ← actual repository for ackrep_core
       ├── .git/
       └── ...

The components  *ackrep_core* and *ackrep_data* are maintained in separate repositories.
It is recommended to clone them separately one level up in the directory structure.

### Deployment Steps:

The deployment process is triggered by the command `python deploy.py <path_to/settings.yml>` and consists of the following steps (not all of them are currently implemented):

- create configuration files such as `site_specific_settings.py` from templates with data from `settings.yml`.
- stop currently running ackrep-related services on the target server
- upload (rsync) all project data
- restart all running ackrep-related services on the target server
- perform tests
