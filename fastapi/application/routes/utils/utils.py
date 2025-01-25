import secrets
import os

def save_prof(file):
    """
    Generates a secure, unique filename for an uploaded file.

    This function takes an uploaded file and generates a new filename that 
    includes a random hexadecimal string as a prefix. This ensures uniqueness 
    and helps prevent file name conflicts on the server.

    Args:
        file (FileStorage): The uploaded file object, typically obtained from 
                            `request.files` in a Flask application.

    Returns:
        str: A new, unique filename in the format `<random_hex><original_extension>`.
             For example, if the uploaded file is `image.png`, the returned filename 
             might be `a3f4b1c9d7e8f9g1.png`.

    Raises:
        None.

    Process:
    - A 16-character hexadecimal string is generated using `secrets.token_hex(8)`.
      This ensures a cryptographically secure, random prefix for the filename.
    - The original file's extension (e.g., `.png`, `.jpg`) is extracted using 
      `os.path.splitext(file.filename)`.
    - The random string and the file's original extension are concatenated to form 
      the new filename.

    Example Usage:
    ```python
    from flask import request

    uploaded_file = request.files['profile_image']
    unique_filename = save_prof(uploaded_file)
    print(unique_filename)  # Output: a3f4b1c9d7e8f9g1.jpg
    ```
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(file.filename)
    raw_fn = random_hex + f_ext
    return raw_fn
