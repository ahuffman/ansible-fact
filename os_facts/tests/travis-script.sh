#! /bin/bash

run_test () {
  # Test run function
  # argument 1 is container name
  # if argument 1 is not passed run as a normal script
  ## Otherwise put the docker exec command in front of everything
  if [$1 -n]
  then
    DOCKER_CMD="docker exec -it $1 /bin/bash -c"
    echo "Container Information for $1:"
  else
    DOCKER_CMD="/bin/bash -c"
    echo "Virtual Machine Information for Ubuntu:"
  fi
  # Spit out our test platform info
  if [$1 -n]
  then
    echo "$1 Container Configuration:"
    docker inspect $1
    echo
  fi
  $DOCKER_CMD 'cat /etc/os-release'
  $DOCKER_CMD 'uname -a'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo "Starting platform tests...'"
  $DOCKER_CMD 'echo "Running on Ansible version:"'
  $DOCKER_CMD 'ansible --version'
  $DOCKER_CMD 'echo "------------------------------------------"'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo "Ansible Configuration \(only changed\):"'
  $DOCKER_CMD 'ansible-config dump --only-changed'
  $DOCKER_CMD 'echo "------------------------------------------"'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo "Collection Content Details:"'
  $DOCKER_CMD 'ls -lh /home/travis/build/ahuffman/ansible-fact/os_facts/tests/collections/ansible_collections/ansible_fact/os_facts'
  $DOCKER_CMD 'ls -alh /home/travis/build/ahuffman/ansible-fact/os_facts/tests/collections/ansible_collections/ansible_fact/os_facts/'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'cd /home/travis/build/ahuffman/ansible-fact/os_facts/tests/'
  $DOCKER_CMD 'pwd'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo "Launching Test Playbook"'
  $DOCKER_CMD 'ansible-playbook test.yml'
  $DOCKER_CMD 'if [$? -ne 0]; then echo "The tests failed."; return 5; fi'
}

# Execute Tests
## Ubuntu VM
UBUNTU=`run_tests`
CENTOS7=`run_tests centos7`
DEBIAN=`run_tests bullseye`

# Return results
if [$UBUNTU -eq 5] || [$CENTOS7 -eq 5] || [$DEBIAN -eq 5]
then
  # bad bad test
  return 5
else
  # very good, very very good
  return 0
fi
