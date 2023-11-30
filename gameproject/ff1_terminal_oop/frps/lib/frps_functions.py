# FRPS+ (Flexible Rock Paper Scissors)
# Functions
import yaml


def convert_yaml_to_ruleset(yaml_content: str):
    """
    Converts YAML data to a ruleset for FRPS (dict)
    :param yaml_content: YAML Data as string
    :return: Dictionary in the format FRPS can understand (or None)
    """
    try:
        ruleset_dict = yaml.safe_load(yaml_content)
        return ruleset_dict
    except yaml.YAMLError as error:
        print(f"Error loading YAML: {error}")
        return None


def load_ruleset_from_file(file_path):
    """
    Reads file from disk and converts it into a format FRPS can understand
    :param file_path: Path to YAML-File
    :return: Dictionary in the format FRPS can understand (or None)
    """
    try:
        with open(file_path, 'r') as file:
            yaml_content = file.read()
            return convert_yaml_to_ruleset(yaml_content)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise


# Example usage:
if __name__ == '__main__':
    ruleset_yaml_example_data = """
    Rock:
      Scissors: crushes
      Lizard: crushes
    Paper:
      Rock: covers
      Spock: disproves
    Scissors:
      Paper: cut
      Lizard: decapitates
    Lizard:
      Paper: eats
      Spock: poisons
    Spock:
      Scissors: smashes
      Rock: vaporizes
    """

    result = convert_yaml_to_ruleset(ruleset_yaml_example_data)
    print("Example Input:")
    print(ruleset_yaml_example_data)
    print("Example Output:")
    print(result)
