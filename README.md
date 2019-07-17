# ansible-fact

## About
The concept of this project is to perform Infrastructure-as-Code in Reverse (i.e. iacir - pronounced: aya sir).  

`ansible-fact` consists of a collection of Ansible fact collectors to be able to generate structured data and harvest system configurations.  The goal is to be able to automatically collect all aspects of a system's configuration through modules.

## Available Modules
| Module Name | Description | Test Playbook |
| --- | --- | --- |
| [scan_cron](library/scan_cron.py) | Collects all cron data from a system and converts to structured data | [scan_cron.yml](test/scan_cron.yml) |
| [scan_sudoers](library/scan_sudoers.py) | Collects all sudoers configurations and converts to structured data | [scan_sudoers.yml](test/scan_sudoers.yml) |
| [scan_user_group](library/scan_user_group.py) | Collects all local user and group data from `/etc/shadow`, `/etc/gshadow`, `/etc/passwd`, and `/etc/group`, and merges into structured data. | [scan_user_group.yml](test/scan_user_group.yml)

## Documentation
All module documentation can be found in each respective module, as with any Ansible module.

## Author
[Andrew J. Huffman](https://github.com/ahuffman)
