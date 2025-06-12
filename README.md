# Extract and Print-to-the-Terminal MIVZAKIM from Y NET

## Installation 

Environment: Needs Python 3.x on Linux

1. Optional: Create and activate a virtual env
2. Run: `pip install -r requirements.txt`
3. Fix the URL in the file `fetch` by removing the redundant space character
4. Optional: Add terms in the list "to_exclude" in the file `fetch`. MIVZAKIM contained this term will be excluded (I.e., not displayed).

## Usage

1. Run the sw: `./fetch`
2. The new (I.e., not yet viewed) MIVZAKIM will be shown
3. At the prompt you have 3 options:
   
   - Press "Enter" to exit
   - Enter a number to see the text associated with this Number
   - Enter two or more numbers, separated by comma(s). The text associated with the numbers entered will be shown and the sw will exit
  # Start recording everything in this terminal
  script

## Typical installation flow

```
  # Change to the home directory
  cd

  # Remove old installation of our sw
  rm -rf y_net_mivzakim

  # Fetch a copy of our sw from github
  git clone https://github.com/shalommmitz/y_net_mivzakim

  # Make the newly-fetched folder our current folder
  cd y_net_mivzakim/
 
  # Fix the URL by removing the "space" character
  sed -i 's/y ne/yne/' fetch

  # Needed only once: install pip and venv machine wide
  sudo apt install python3-pip python3-venv

  # Create the virtual environment. This actually create a sub-folder named 'venv'
  python3 -m venv venv

  # Activate the virtual environment. i
  #This means any Python packages we install using pip will be installed only for this project
  . v

  # Install the needed packages
  pip install -r requirements.txt 

  # Make our script executable, so we can run it
  chmod +x fetch

  # Run the script
  ./fetch
```

## License

   MIT
