import re


def extract_defined_config(config):
    """Extract defined configuration out of SAN config."""

    # matches everything starting with  "Defined configuration"
    # text until it finds an empty line.
    regex = r'^(Defined configuration:.+?\n)$'
    match = re.search(regex, config, re.M|re.S)
    defined_config = match.group(1)

    return defined_config


def extract_effective_config(config):
    """Extract effective configuration out of SAN config."""

    # matches everything starting with  "Effective configuration"
    # text until it finds an empty line
    regex = r'^(Effective configuration:.+?\n)$'
    match = re.search(regex, config, re.M|re.S)
    defined_config = match.group(1)

    return defined_config


def extract_alias_config(defined_config):
    """Extract alias configuration block out the defined configuration."""

    regex = '(^ alias.*?\n)$'
    match = re.search(regex, defined_config, re.M|re.S)

    return match.group(1)


def parse_alias(alias):
    """Parse an alias string and return it as a dictionary.

    Input:
    alias01
        AA:AA:AA:AA:AA:AA:AA:AA
        BB:BB:BB:BB:BB:BB:BB:BB

    Output:
    {'alias01': [
        'AA:AA:AA:AA:AA:AA:AA:AA',
        'BB:BB:BB:BB:BB:BB:BB:BB',
    ]}
    """

    # Clean up the string and split values onto a list
    alias = alias.strip('\n').replace(' ', '')
    alias = alias.split('\n')
    # Alias name is contained in the first element of the list
    alias_name = alias[0]
    # All elements but first will be WWPNs for that alias
    wwpns = alias[1:]

    return {alias_name: wwpns}


def get_aliases(config):
    """Get all aliases of the given SAN configuration and returns them as a
    dictionary with their respective WWPNs.
    """

    aliases = {}
    # Extract the defined configuration
    defined_config = extract_defined_config(config)
    # Extract the section containing the aliases
    alias_block = extract_alias_config(defined_config)

    # Separate each alias onto an item of a list and proceed with parsing
    # discard the first element as there is no need to build the original
    # content back
    match = re.split(' alias: ', alias_block)
    for alias in match[1:]:
        aliases.update(parse_alias(alias))

    return aliases


def alias_exist(alias, aliases):
    """Check if the alias name exist on the defined aliases config."""

    if alias in aliases:
        return True
    else:
        return False


def main():
    pass


if __name__ == '__main__':
    main()