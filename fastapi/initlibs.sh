#!/bin/bash

# Define the input requirements.txt and output file.txt
REQUIREMENTS_FILE="requirements.txt"
OUTPUT_FILE="file.txt"

# Ensure the output file is empty before starting
> $OUTPUT_FILE

# Function to install a package
install_package() {
	    PACKAGE_NAME=$1
	        PACKAGE_VERSION=$2

		    # Install the package with pip
		        if pip install "$PACKAGE_NAME==$PACKAGE_VERSION"; then
				        echo "$PACKAGE_NAME==$PACKAGE_VERSION installed successfully."
					    else
						            # If installation fails, log the package to the output file
							            echo "$PACKAGE_NAME==$PACKAGE_VERSION" >> $OUTPUT_FILE
								            echo "Failed to install $PACKAGE_NAME==$PACKAGE_VERSION, logged in $OUTPUT_FILE."
									        fi
									}

								# Loop through each line in the requirements.txt file
								while IFS= read -r line || [[ -n "$line" ]]; do
									    # Split the package name and version (assuming format is package==version)
									        if [[ "$line" =~ ^([a-zA-Z0-9_-]+)==([0-9\.]+)$ ]]; then
											        PACKAGE_NAME="${BASH_REMATCH[1]}"
												        PACKAGE_VERSION="${BASH_REMATCH[2]}"
													        install_package "$PACKAGE_NAME" "$PACKAGE_VERSION"
														    else
															            echo "Skipping invalid line in requirements.txt: $line"
																        fi
																done < "$REQUIREMENTS_FILE"

																echo "Package installation complete. Check $OUTPUT_FILE for any packages that failed to install."

