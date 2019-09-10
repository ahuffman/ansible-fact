# ansible-fact
[![Build Status](https://travis-ci.com/ahuffman/ansible-fact.svg?branch=dev)](https://travis-ci.com/ahuffman/ansible-fact)

## Table of Contents
|Collection|Description|Documentation|
|---|---|---|
|os_facts| Ansible Galaxy collection of Operating System fact collectors|[os_facts/docs/README.md](os_facts/docs/README.md)|
|application_facts| Ansible Galaxy collection of Application specific fact collectors | [application_facts/docs/README.md](application_facts/docs/README.md)|

## Automated Testing
Testing is automated by using Travis-CI.  
All tests are contained in each collection's `tests` directory.  
Tests are run against a series of OS platforms, either in a virtual machine (Ubuntu specific) or in a docker container.  
Testing containers are automatically pre-built with Ansible and any required Python dependencies out of the [ansible-fact-testing-containers](https://github.com/ahuffman/ansible-fact-testing-containers) repository.

## Authors
[Andrew J. Huffman](https://github.com/ahuffman)  
[John Westcott IV](https://github.com/john-westcott-iv)

## License
GPL3.0+
