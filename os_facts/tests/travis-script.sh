#! /bin/bash

echo "Running on Ansible version:"
ansible-playbook --version
echo "------------------------------------------"

# TEMP Travis Testing
echo "Collection Content:"
ls -lh /root/ansible-fact/os_facts/tests/collections/ansible_collections/ansible_fact/os_facts
ls -alh /root/ansible-fact/os_facts/tests/collections/ansible_collections/ansible_fact/os_facts/
echo
echo

cd /root/ansible-fact/os_facts/tests/
# display working dir
pwd
echo
echo "Launching Test Playbook"

ansible-playbook test.yml
