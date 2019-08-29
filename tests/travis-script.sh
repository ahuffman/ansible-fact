#! /bin/bash

echo "Running on Ansible version"
ansible-playbook --version
echo "------------------------------------------"

cd /root/ansible-fact/tests/
# display working dir
pwd
ansible-playbook test.yml
