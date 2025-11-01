# Get a field value from a .env file
def get_environment_field(env_path, key):
    """Read the .env file at env_path and return the value for the given key, or None if not found."""
    if not os.path.exists(env_path):
        print(f".env file not found at {env_path}")
        return None
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                if k.strip() == key:
                    return v.strip()
    return None

# Convert dash-separated to CamelCase
def dash_to_camel(name):
    parts = name.split('-')
    return ''.join(word.capitalize() for word in parts)

# Convert dash-separated to underscore_lowercase
def dash_to_underscore(name):
    return name.replace('-', '_').lower()