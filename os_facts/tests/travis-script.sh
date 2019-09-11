#! /bin/bash

run_tests () {
  # Test run function
  # argument 1 is container name
  # if argument 1 is not passed run as a normal script
  ## Otherwise put the docker exec command in front of everything
  if [ ! -z "$1" ]
  then
    DOCKER_CMD="docker exec -it -u travis $1 /bin/bash -c"
    echo Container Information for $1:
  else
    DOCKER_CMD="/bin/bash -c"
    echo Virtual Machine Information for Ubuntu:
  fi
  # Spit out our test platform info
  if [ ! -z "$1" ]
  then
    echo $1 Container Configuration:
    docker inspect $1
    echo
  fi
  $DOCKER_CMD 'cat /etc/os-release'
  $DOCKER_CMD 'uname -a'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo Starting platform tests...'
  $DOCKER_CMD 'echo Running on Ansible version:'
  $DOCKER_CMD 'ansible --version'
  $DOCKER_CMD 'echo "------------------------------------------"'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo Ansible Configuration \(only changed\):'
  $DOCKER_CMD 'ansible-config dump --only-changed'
  $DOCKER_CMD 'echo "------------------------------------------"'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo "Collection Content Details:"'
  $DOCKER_CMD 'ls -lh /home/travis/build/ahuffman/ansible-fact/os_facts/tests/collections/ansible_collections/ansible_fact/os_facts'
  $DOCKER_CMD 'ls -alh /home/travis/build/ahuffman/ansible-fact/os_facts/tests/collections/ansible_collections/ansible_fact/os_facts/'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo'
  $DOCKER_CMD 'echo Launching Test Playbook'
  $DOCKER_CMD 'cd /home/travis/build/ahuffman/ansible-fact/os_facts/tests/;pwd;echo;ansible-playbook test.yml -u travis; PLAYRESULT=$?'
  $DOCKER_CMD 'if [ $PLAYRESULT -ne 0 ]; then echo The tests failed.; return 5; else echo The tests passed.; return 0; fi'
}

collect_results () {
  if [ $UBUNTU -ne 0 ] || [ $CENTOS7 -ne 0 ] || [ $DEBIAN -ne 0 ]
  then
    # bad bad test
    echo Some tests failed:
    echo Ubuntu Result: $UBUNTU
    echo CentOS7 Result: $CENTOS7
    echo Debian Result: $DEBIAN
    return 5
  else
    # very good, very very good
    echo All tests passed!
    return 0
  fi
}

# Execute Tests
## Ubuntu VM
# UBUNTU=`run_tests`
# CENTOS7=`run_tests centos7`
# DEBIAN=`run_tests bullseye`
run_tests
run_tests centos7
run_tests bullseye
# Return Test results to Travis
# collect_results
