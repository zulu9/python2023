import yaml

def load_yaml_to_dict(yaml_str):
    try:
        data_dict = yaml.safe_load(yaml_str)
        return data_dict
    except yaml.YAMLError as e:
        print(f"Error loading YAML: {e}")
        return None

# Example usage:
yaml_data = """
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

result_dict = load_yaml_to_dict(yaml_data)
print(result_dict)
