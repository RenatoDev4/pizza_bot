from typing import Optional


def load_info(file_name: str) -> Optional[str]:
    """
    Load and return the contents of a file.

    Args:
        file_name (str): The name of the file to load.

    Returns:
        Optional[str]: The contents of the file, or None if there was an error loading the file.
    """
    try:
        with open(file_name, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Error loading file: {e}")
        return None


def save(file_name: str, content: str) -> None:
    """
    Save the given content to the specified file.

    Args:
        file_name (str): The name of the file to save the content to.
        content (str): The content to be saved to the file.

    Returns:
        None
    """
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Error saving file: {e}")
        return None
