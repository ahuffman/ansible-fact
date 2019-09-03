#! /bin/bash

echo "Running on Ansible version:"
ansible --version
echo "------------------------------------------"
echo
echo "Ansible Configuration (only changed):"
ansible-config dump --only-changed
echo "------------------------------------------"
echo
echo

# TEMP Travis Testing
echo "Collection Content Details:"
ls -lh /home/travis/build/ahuffman/ansible-fact/os_facts/tests/collections/ansible_collections/ansible_fact/os_facts
ls -alh /home/travis/build/ahuffman/ansible-fact/os_facts/tests/collections/ansible_collections/ansible_fact/os_facts/
echo
echo

cd /home/travis/build/ahuffman/ansible-fact/os_facts/tests/
# display working dir
pwd
echo
echo "Launching Test Playbook"

ansible-playbook test.yml
