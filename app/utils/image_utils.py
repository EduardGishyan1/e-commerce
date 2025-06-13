def generate_mock_image_url(size: int = 150) -> str:
    """
    Generate a mock image URL using placeholder service.
    
    Args:
    - size (int): The size of the square image (e.g., 150 for 150x150).

    Returns:
    - str: URL of the generated image.
    """
    return f"https://via.placeholder.com/{size}"