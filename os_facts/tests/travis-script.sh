#! /bin/bash
# This script will exit 5 if any platform tests fail

run_tests() {
  # set this to non-zero so we don't get false positives from builds
  PLAYRESULT=1
  # Test run function
  # argument 1 is container name
  # if argument 1 is not passed run as a normal script
  ## Otherwise put the docker exec command in front of everything
  # Returns PLAYRESULT
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
  $DOCKER_CMD 'cd /home/travis/build/ahuffman/ansible-fact/os_facts/tests/;pwd;echo;ansible-playbook test.yml -u travis;'
  PLAYRESULT=$?
}

set_result() {
  if [ $PLAYRESULT -eq 0 ]
  then
    echo 0
  else
    echo 5
  fi
}

collect_results () {
  if [ $UBUNTU -ne 0 ] || [ $CENTOS7 -ne 0 ] || [ $DEBIAN -ne 0 ]
  then
    # bad bad test
    echo
    echo
    echo Some tests failed:
    echo ' _____________________'
    echo '| Platform | Exit Code |'
    echo "|  Ubuntu  |     $UBUNTU     |"
    echo "|  CentOS7 |     $CENTOS7     |"
    echo "|  Debian  |     $DEBIAN     |"
    exit 5
  else
    # very good, very very good
    echo
    echo
    echo All tests passed!
    exit 0
  fi
}

# Execute Tests
## Ubuntu VM
run_tests
UBUNTU=`set_result`
## CentOS7 Container
run_tests centos7
CENTOS7=`set_result`
## Debian Bullseye Container
run_tests bullseye
DEBIAN=`set_result`

# Return Test results and exit to Travis
collect_results
