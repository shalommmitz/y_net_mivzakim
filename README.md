# y_net_mivzakim

A Python utility to fetch and process news headlines ("מבזקים") from the ynet's site. Designed for quick and structured access to the most recent headlines, optionally filtering out irrelevant ones based on exclusion terms.

## Features

- Downloads the latest headlines
- Filters out unwanted headlines using user-defined keywords
- Command-line interface to see more details on choosen items
- Customizable exclusion terms list

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/shalommmitz/y_net_mivzakim.git
   cd y_net_mivzakim
   ```

2. (Optional but recommended) Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Make sure you're inside the project directory:

   ```bash
   cd y_net_mivzakim
   ```

2. Run the main script:

   ```bash
   python3 ynet_mivzakim.py
   ```

3. The items not-yet-seen will be displayed. At the prompt, you can do one of the following: 

   - Hit "Enter" to refresh
   - Enter a list of item-number (coma separed) to see details.
   - `q` to quit

## Configuration: Exclude Terms

To filter out certain types of news, add exclusion terms to `exclude.txt`, one per line. Example:

```
ספורט
פרסומת
פאניקה
מזג האוויר
```

These terms will be matched (case-sensitive) against the headlines.

## Typical Flow

```bash
git clone https://github.com/shalommmitz/y_net_mivzakim.git
cd y_net_mivzakim
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 ynet_mivzakim.py
cat headlines.txt
```

## License

MIT License. See `LICENSE` file for details.

## Contributing

Pull requests and suggestions are welcome!
