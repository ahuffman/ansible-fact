
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.facts.system import distribution
import re

class FactGatherer(AnsibleModule):
    def remove_comment(self, line, comment_characters):
        return re.sub('[{}].*'.format(comment_characters), '', line)

    def doDefault(self):
        self.fail_json("No default method was defined for this class")

    def __init__(self, argument_spec, **kwargs):
        # If we have any global arguments, here is would we put them
        args = dict(
        )
        args.update(argument_spec)

        mutually_exclusive = kwargs.get('mutually_exclusive', [])
        kwargs['mutually_exclusive'] = mutually_exclusive.extend((
        ))

        super(FactGatherer, self).__init__(argument_spec=args, **kwargs)

    def main(self):
        distro_facts = distribution.DistributionFactCollector()
        os_facts = distro_facts.collect(self)
        os_family = os_facts['os_family']
        distro = os_facts['distribution']
        distribution_release = os_facts['distribution_release']
        distribution_major_version = os_facts['distribution_major_version']

        prescidence = [
            "{}{}{}".format(os_family,distro,distribution_release),
            "{}{}{}".format(os_family,distro,distribution_major_version),
            "{}{}".format(os_family,distro),
            "{}".format(os_family),
        ]

        for ordered_item in prescidence:
            method_name = "do{}".format(ordered_item)
            if hasattr(self, method_name):
              self.debug("Selected method {}".format(method_name))
              return getattr(self, method_name)()

        self.warn('No spcific task was found to handle {}/{}/{} attempting to use default gather'.format(os_family, distro, distribution_release))
        return self.doDefault()
