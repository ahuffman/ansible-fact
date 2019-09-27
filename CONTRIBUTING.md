# Contributing
To contribute to this project please fork the repository, make your changes and issue a pull request.

Here are some general things to know about contributing.

## Custom Module Creation
### Our Base Class
If you need to create a new module we have a base class to start from called [FactGatherer](/ahuffman/ansible-fact/blob/dev/os_facts/plugins/module_utils/fact_gatherer.py).

### Implementing Our Base Class
This base class extends AnsibleModule and is intended to be used as a starting point for your new module. To start, include our module like this:
``` python
from ansible_collections.ansible_fact.os_facts.plugins.module_utils.fact_gatherer import FactGatherer
```

Next, create your own class with FactGatherer as a parent class:
```python
class MyGatherer(FactGatherer):
```

Then, in your modules main function will create and execute your new class. In this example, your class will take two parameters: param1 (a list) and param2 (a bool). The parameters passed here are subquently passed into AnsibleModule as the argument spec:
```python
def main():
    module = MyGatherer(
        dict(
            param1=dict(type='list', default=[], required=False),
            param2=dict(type='bool', default=False, required=False),
        ),
        supports_check_mode=True
    )
    module.main()
```

Inside your class you will use an init method to extract the AnsibleModule parameters into  variables for your class:
 ```python
     def __init__(self, argument_spec, **kwargs):
        # Call the parent constructor
        super(CronGatherer, self).__init__(argument_spec=argument_spec, **kwargs)
        # Extract the module params into class variables
        self.param1 = self.params.get('param1')
        self.param2 = self.params.get('param2')
        # Set additional class variables
        self.my_constant1 = 3.14
```

### Determining OS behaviour
The main method implemented by FactGather has  logic in that tries to find a method in your class to execute on the target system. To do this, it uses the following OS facts Ansible finds for the tharget system:
* OS Family
* Distribution
* Distribution Release
* Distribution Major Version

As an example, lets say we are running with the following values:
|Fact|Value|
|---|---|
|OS Family|Linux|
|Distribution|RedHat|
|Distribution Release|7.7.2|
|Distribution Major Version|7|

With these inputs it would execute the first method it finds with the following name:
* doLinuxRedHat7_7_2
* doLinuxRedHat7
* doLinuxRedHat
* doLinux

__NOTE:__ Any . characters in a version are changed to _ as a . is not a valid character in a method name.

This allows you to customize your fact gatheering on different OS familys, releases of those OSes, etc. Notice that it searches from the most specific case to the most generic. So if a new release of an OS changes the way fact gather needs to be done your code can compensate for those changes.

### Default Behaviour
If your class does not implement a method that matches the target machine FactGatherer will take the following action:
```python
        self.warn('No spcific task was found to handle {}/{}/{} attempting to use default gather'.format(os_family, distro, distribution_release))
        return self.doDefault()
```

 The doDefauult method is defined in the GetherFacts class as:
```python
    def doDefault(self):
        self.fail_json("No default method was defined for this class")
```

Your class can (and should) override the doDefault method in FactGatherer.

__Note:__ failure to override the doDefault method in your class will cause a module failure on a machine which does not match one of the specified methods.

Since many *NIX systems have identical implementations of subsystems you may want to put that code into your doDefault method and reference that method from other specific methods.

For example, let's say that your doDefault method has been tested and works on both Linux/Debain and Linux/RHEL and you think it will also work for most other systems. You could do something like this:
```python
def doLinuxRHEL(self):
    self.doDefault(self)

def doLinuxDebain(self):
    self.doDefault(self)

def doDefault(self):
    ... do some tasks ...
```

This would make it so that RHEL and Debain would *not* print the "No specific task was found to handle.." message but any other systems (i.e. Darwin) would print the message but all nodes would execute the same collection code.

### Returning Data
At the end of your fact gathering code you should return your findings as ansible_facts with a meaningful name. The following is a return example from the cron fact gatherer:
```python
self.exit_json(**{ 'ansible_facts': {'cron': cron } })
```

### Other Useful Methods
In addition to executing the method which matches the target server, the GatherFacts class can also contain useful methods which can be shared across the fact gatherers.

These helper methods will be at the top of the class for easy reference.

For example, there is a remove_comment method specified as:
```python
def remove_comment(self, line, comment_characters):
```
This method will remove comments from a line as specified by the characters in its second parameter. So you could do something like:
```python
self.remove_comment(line_from_file, '#')
```
To remove anything from a # character onward. If your file type can specify comments as either # or ! you could do:
```python
self.remove_comment(line_from_file, '#!')
```
__NOTE:__ (The order of the characters are not important)
