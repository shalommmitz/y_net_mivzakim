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

## License

   MIT
