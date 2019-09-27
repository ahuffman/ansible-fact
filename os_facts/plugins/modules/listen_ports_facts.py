#!/usr/bin/python

# Copyright: (c) 2019, Andrew J. Huffman <ahuffman@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: netstat_facts
short_description: Collect information from netstat
version_added: "2.8"
description:
    - "Collects results of netstat."
options:
    output_parsed_configs:
        description:
            - Parse the results
        default: True
        required: False
author:
    - Andrew J. Huffman (@ahuffman)
    - John Westcott IV (@john-westcott-iv)
'''

EXAMPLES = '''
- name: "Collect all netstat data"
  netstat_facts:

- name: "Dont parse output, only show raw data"
  netstat_facts:
    output_parsed_configs: False
'''

RETURN = '''
all_scanned_files:
  - configuration: The file scanned as a list
    data:
      schedules:
        - day_of_month: The day of the month of the schedule
          day_of_week: The day of the week of the schedule
          hour: The hour of the schedule
          minute: The minute of the schedule
          month: The month of the schedule
          timeframe: If specified as @yearly/hourly/reboot/monthly
          command: The command to be run
      variables:
        - name: name of the variable
          value: The value of the variable
    path: The file that this information was parsed from
allow:
  path: The path to allow file
  users: List of users in the allow file
deny:
  path: The path to the deny file
  users: List of users in the deny file
files:
  - name: The file name scanned
    user:
    group:
    permissions:
'''

from ansible_collections.ansible_fact.os_facts.plugins.module_utils.fact_gatherer import FactGatherer
from os.path import isfile
from os import access, X_OK
import re

class NetstatGatherer(FactGatherer):
    #def doLinux(self):
    #    command = self.findCommand('netstat')
    #    try:
    #        rc, stdout, stderr = self.run_command([command, '-plunt'])
    #    except Exception as e:
    #        self.fail_json(msg="Failed to run {}: {}".format(command, e))
#
#        self.exit_json(**{ 'ansible_facts': {'cron': cron } })


    def doAIX(self):
        command = self.findCommand('lsof')
        try:
            rc, stdout, stderr = self.run_command([command, '+c0 -i 2'])
        except Exception as e:
            self.fail_json(msg="Failed to run {}: {}".format(command, e))

        if rc != 0:
            self.fail_json(msg='Failed to run {} successfully: {}'.format(command, rc))

        if not self.parse_configs:
            self.exit_json(**{'lsof_stdout_lines': stdout.split('\n')})

        re_listen_ports = re.compile(r'^(?P<cmd>[^\s]+)\s+(?P<pid>[0-9]+)\s+(?P<user>[^\s]+)\s+(?P<fd>\d+[^\s]+)\s+(?P<type>[^\s]+)\s+(?P<dev>[^\s]+)\s+(?P<size>[^\s]+)\s+(?P<node>[^\s]+)\s+(?P<name>[^\s]+)( \((?P<state>[^\(]+)\)){0,1}$')

        listen_ports = []
        for line in stdout.split('\n'):
            line_match = re_listen_ports.search(line)
            if line_match != None:
                port = {
                    'cmd': line_match.group('cmd'),
                    'pid': line_match.group('pid'),
                    'user': line_match.group('user'),
                    'fd': line_match.group('fd'),
                    'type': line_match.group('type'),
                    'dev': line_match.group('dev'),
                    'size': line_match.group('size'),
                    'node': line_match.group('node'),
                    'name': line_match.group('name'),
                    'state': line_match.group('state'),
                }
    
                if port['node'] == 'UDP' or (port['node'] == 'TCP' and port['state'] == 'LISTEN'):
                    listen_ports.append(port)

        self.exit_json(**{ 'ansible_facts': {'listening_ports': listen_ports} })

    #def doDarwin(self):
    #    command = self.findCommand('lsof')
    #    try:
    #        rc, stdout, stderr = self.run_command([command, '+c0'])
    #        with open('/tmp/john', 'w') as f:
    #            f.write("RC\n{}".format(rc))
    #            f.write("stdout\n{}".format(stdout))
    #            f.write("stderr\n{}".format(stderr))
    #        self.exit_json(**{ 'ansible_facts': {'listening_ports': stdout} })
    #    except Exception as e:
    #        self.fail_json(msg="Failed to run {}: {}".format(command, e))


    def __init__(self, argument_spec, **kwargs):
        # Call the parent constructor
        super(NetstatGatherer, self).__init__(argument_spec=argument_spec, **kwargs)
        # Extract the module params into class variables
        self.parse_configs = self.params.get('output_parsed_configs')
        # Set additional class variables



def main():
    module = NetstatGatherer(
        dict(
            output_parsed_configs=dict(type='bool', default=True, required=False),
        ),
        supports_check_mode=True
    )
    module.main()


if __name__ == '__main__':
    main()
