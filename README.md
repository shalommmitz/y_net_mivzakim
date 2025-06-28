# y_net_mivzakim

A pure terminal utility to fetch and display news headlines ("מבזקים") from the ynet's site. Designed for quick and structured access to the most recent headlines, optionally filtering out irrelevant ones based on exclusion terms. Items are shown only once ! For the terminal lovers.

## Features

- Downloads the latest headlines
- Filters out unwanted headlines using user-defined keywords
- TUI or pure Command-line interfaces to see more details on chosen items

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shalommmitz/y_net_mivzakim.git
   cd y_net_mivzakim
   ```

2. (Optional but recommended) Create a virtual environment:

   ```bash
   python3 -m venv venv
   . venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   sudo apt install libicu-dev
   pip install -r requirements.txt
   ```

## Using the "Elegant TUI" version:

1. Make sure you're inside the project directory:

   ```bash
   cd y_net_mivzakim
   ```

2. Activate the virtual environment:

   ```bash
   . v
   ```
   
3. Run the main script:

   ```bash
   ./mivzakim
   ```

   The items not-yet-seen will be displayed.

4. Click on the down-arrow next to each item to see the full text

5. Press 'r' to refresh. Press 'q' to quit

   Or just click with your mouse. Yes, on terminal. And yes, you can SSH it :)

## Using the "Pure CLI" version:

1. Make sure you're inside the project directory:

   ```bash
   cd y_net_mivzakim
   ```

2. Activate the virtual environment:

   ```bash
   . v
   ```
   
3. Run the main script:

   ```bash
   ./mivzakim_cli
   ```
  
   or
   ```bash
   python mivzakim_cli
   ```

4. The items not-yet-seen will be displayed.  

5. Interaction with the sw:

   At the prompt, you can do one of the following:

   - Hit "Enter" to refresh
   - Enter a list of item-number(s) (comma separated) to see details or the requested items.
   - `q` to quit

## Configuration: Exclude Terms

To filter out certain types of news, add exclusion terms to the file `terms_to_exclude.txt`, one per line. Example:

```
ספורט
פרסומת
NBA
```

These terms will be matched (case-sensitive) against the headlines.

## An example of the installation and launch steps

```bash
git clone https://github.com/shalommmitz/y_net_mivzakim.git
cd y_net_mivzakim
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 mivzakim
```

## License

MIT License. See [LICENSE](LICENSE ) file for details.

## Contributing

Pull requests and suggestions are welcome!
