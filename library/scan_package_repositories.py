#!/usr/bin/python

# Copyright: (c) 2019, Andrew J. Huffman <ahuffman@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: scan_package_repositories
short_description: Collects all package repositories on a system
version_added: "2.8"
description:
    - "Collects the repository data from package repositories on a system."
    - "This module presents the package repository data and returns the configuration data as ansible_facts"

author:
    - Andrew J. Huffman (@ahuffman)
'''

EXAMPLES = '''

'''

RETURN = '''

'''

from ansible.module_utils.basic import AnsibleModule
import ansible.module_utils.facts.system.distribution as dist
import os, re, platform
from os.path import isfile, isdir, join

def main():
    module_args = dict(
        output_ps_stdout_lines=dict(
            type='bool',
            default=False,
            required=False
        ),
        output_parsed_processes=dict(
            type='bool',
            default=True,
            required=False
        )
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    params = module.params

    def get_yum_repodata():
        yum_repos = list()
        return yum_repos


    # def get_deb_repodata():


    # Do work
    ## Get OS family by recycling ansible distro code
    distro_facts = dist.DistributionFactCollector()
    os_facts = distro_facts.collect(module)
    os_family = os_facts['os_family']

    ## Enterprise Linux - based
    if os_family == "RedHat":
        repos = get_yum_repodata()

    ## Debian Linux - based
    # if os_family == "Debian":

    ## Suse
    # if os_family == "Suse":

    ## Archlinux

    ## Mandrake

    ## Solaris

    ## Slackware

    ## Altlinux

    ## SGML

    ## Gentoo

    ## Alpine

    ## AIX

    ## HP-UX

    ## Darwin

    ## FreeBSD

    ## ClearLinux


    # Build output
    repositories = dict()
    repositories['os_family'] = os_family
    repositories['repositories'] = repos

    result = {'ansible_facts': {'package_repositories': repositories }}

    module.exit_json(**result)


if __name__ == '__main__':
    main()
