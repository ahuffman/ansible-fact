#! /bin/bash

echo "Running on Ansible version"
ansible-playbook --version
echo "------------------------------------------"

# TEMP Travis Testing
echo "****************** TEMP TESTING ************************"
ls /root/.ansible/collections/ansible_collections/john_westcott_iv/ansible_fact
echo "****************** END TEMP TESTING ************************"

cd /root/ansible-fact/tests/
# display working dir
pwd
ansible-playbook test.yml
