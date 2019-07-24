# ansible-fact
## Table of Contents
<!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:1 -->

1. [Table of Contents](#table-of-contents)
2. [About](#about)
3. [Available Modules](#available-modules)
4. [Module Documentation](#module-documentation)
5. [Contributions](#contributions)
	1. [Guidelines](#guidelines)
6. [Author(s)](#authors)

<!-- /TOC -->

## About
The concept of this project is to perform Infrastructure-as-Code in Reverse (i.e. iacir - pronounced: aya sir).  

`ansible-fact` consists of a collection of Ansible fact collectors to be able to generate structured data and harvest system configurations.  The goal is to be able to automatically collect all aspects of a system's configuration through modules.

## Available Modules
| Module Name | Description | Test Playbook |
| --- | --- | --- |
| [scan_cron](library/scan_cron.py) | Collects all cron data from a system and converts to structured data | [scan_cron.yml](test/scan_cron.yml) |
| [scan_package_repositories](library/scan_package_repositories.py) | Collects configured package repository data from a system and converts to structured data. | [scan_package_repositories.yml](test/scan_package_repositories.yml) |
| [scan_processes](library/scan_processes.py) | Collects currently running processes from a system and converts to structured data | [scan_processes.yml](test/scan_processes.yml) |
| [scan_sudoers](library/scan_sudoers.py) | Collects all sudoers configurations and converts to structured data | [scan_sudoers.yml](test/scan_sudoers.yml) |
| [scan_user_group](library/scan_user_group.py) | Collects all local user and group data from `/etc/shadow`, `/etc/gshadow`, `/etc/passwd`, and `/etc/group`, and merges into structured data. | [scan_user_group.yml](test/scan_user_group.yml)

## Module Documentation
All module documentation can be found in each respective module, as with any Ansible module.

## Contributions
Please feel free to openly contribute to this project.  All code will be reviewed prior to merging.

### Guidelines
* Please perform all development and pull requests against the `dev` branch of this repository.
* If a particular fact collector can apply to many different Operating Systems, please try and accommodate all Operating System implementations in an attempt to keep this project platform agnostic.
* Please include a test playbook in the [test](test) directory.
* Please place your modules in the [library](library) directory.
* Please document your code and modules thoroughly via comments and by following [Ansible's Module Development Documentation](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#starting-a-new-module).

## Author(s)
[Andrew J. Huffman](https://github.com/ahuffman)
