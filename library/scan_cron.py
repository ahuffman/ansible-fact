#!/usr/bin/python

# Copyright: (c) 2019, Andrew J. Huffman <ahuffman@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: scan_cron
short_description: Collects cron job facts
version_added: "2.8"
description:
    - "Collects cron job facts about a system"
options:
    output_raw_configs:
        description:
            - Whether or not to output raw configuration lines (excluding comments) from the scanned sudoers files
        default: True
        required: False
    output_parsed_configs:
        description:
            - Whether or not to output parsed data from the scanned cron files
        default: True
        required: False
author:
    - Andrew J. Huffman (@ahuffman)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_new_test_module:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_new_test_module:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_new_test_module:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
    returned: always
message:
    description: The output message that the sample module generates
    type: str
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
import os
from os.path import isfile, isdir, join
import re

def main():
    module_args = dict(
        output_raw_configs=dict(
            type='bool',
            default=True,
            required=False
        ),
        output_parsed_configs=dict(
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

    def get_cron_allow():
        allow = dict()
        allow['path'] = '/etc/cron.allow'
        allow['users'] = list()
        try:
            cron_allow = open('/etc/cron.allow', 'r')
            for line in cron_allow:
                user = line.replace('\n', '')
                allow['users'].append(user)
            cron_allow.close()
        except:
            pass
        return allow

    def get_cron_deny():
        deny = dict()
        deny['path'] = '/etc/cron.deny'
        deny['users'] = list()
        try:
            cron_deny = open('/etc/cron.deny', 'r')
            for line in cron_deny:
                user = line.replace('\n', '')
                deny['users'].append(user)
            cron_deny.close()
        except:
            pass
        return deny

    def get_cron_files():
        # standard cron locations for cron file discovery
        cron_paths = [
            "/etc/crontab"
        ]
        cron_dirs = [
            "/etc/cron.hourly",
            "/etc/cron.daily",
            "/etc/cron.weekly",
            "/etc/cron.monthly",
            "/var/spool/cron",
            "/etc/cron.d"
        ]

        # Look for files in cron directories and append to cron_paths
        for dir in cron_dirs:
            try:
                cron_paths += [join(dir, filename) for filename in os.listdir(dir) if isfile(join(dir, filename))]
                # keep digging
                cron_dirs += [join(dir, filename) for filename in os.listdir(dir) if isdir(join(dir, filename))]
            except:
                pass
        return cron_paths

    def get_cron_data(cron_paths):
        # Output data
        cron_data = list()
        # Regex for parsing data
        variable_re = re.compile(r'^.*=.*$')
        comment_re = re.compile(r'^#+')
        shebang_re = re.compile(r'^(#!\/){1}.*$')

        # work on each file that was found
        for cron in cron_paths:
            job = dict()
            job['path'] = cron
            job['configuration'] = list()
            try:
                config = open(cron, 'r')
                for l in config:
                    line = l.replace('\n', '').replace('\t', '    ')
                    # raw configuration output
                    if params['output_raw_configs']:
                        if comment_re.search(line) is None and line != '' and line != None and line != '\r':
                            job['configuration'].append(str(line))
                        elif shebang_re.search(line) and line != '' and line != None and line != '\r':
                            job['configuration'].append(line)
                config.close()
                # append each parsed file
                cron_data.append(job)
            except:
                pass

        return cron_data

    # Do work
    cron_allow = get_cron_allow()
    cron_deny = get_cron_deny()
    cron_paths = get_cron_files()
    cron_data = get_cron_data(cron_paths)

    # Build output
    cron = dict()
    cron['cron_allow'] = cron_allow
    cron['cron_deny'] = cron_deny
    cron['all_scanned_files'] = cron_paths
    cron['cron_files'] = cron_data
    result = {'ansible_facts': {'cron': cron}}

    module.exit_json(**result)


if __name__ == '__main__':
    main()
