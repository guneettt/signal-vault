# SignalVault - Emergency Information Hub

## ***Currently undergoing a few changes/updates.***

An offline emergency information search system that provides quick access to critical survival guides, first aid manuals, and emergency protocols when internet access may be unavailable.

## Features

- **🔍 Offline Document Search**: TF-IDF based search through emergency documents
- **🆘 Emergency Quick Access**: Instant checklists for common emergency scenarios
- **📱 Responsive Design**: Modern dark theme optimized for all devices
- **⚡ Fast Performance**: Cached indexing for instant search results
- **📚 Comprehensive Library**: First aid manuals, survival guides, and emergency protocols

## Screenshots *will be updated soon*

### Landing Page
<img width="942" height="616" alt="Screenshot 2025-07-15 at 4 58 55 PM" src="https://github.com/user-attachments/assets/aaa1c941-7f3e-43d8-b13a-899b3a41a87d" />


### Search Results
*updating

## Quick Start

```bash
# Clone the repository
git clone https://github.com/guneettt/signal-vault.git
cd signal-vault

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000`

## Installation & Setup

### Prerequisites

- **Python 3.9+** (tested on Python 3.9.6)
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/guneettt/signal-vault.git
   cd signal-vault
   ```

2. **Create Virtual Environment**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # On macOS/Linux:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify Installation**
   ```bash
   python app.py
   ```

5. **Access the Application**
   - Open your web browser
   - Navigate to `http://127.0.0.1:5000`
   - Start searching for emergency information!

### Alternative: Command Line Interface

For a lightweight, terminal-only experience:
```bash
python main.py
```

## Usage

### Web Interface
- **Search**: Type keywords like "CPR", "first aid", "water purification"
- **Quick Access**: Click emergency scenario buttons for instant help
- **Keyboard Shortcuts**: Press `Ctrl+K` to focus the search bar
- **Suggestions**: Use the suggestion chips below the search bar

### Emergency Scenarios
- 🌊 **Flood**: Immediate flood response steps
- 🏠 **Earthquake**: Drop, cover, and hold procedures
- 🔥 **Fire**: Building fire evacuation and safety
- 🫁 **Breathing Issues**: CPR and airway management
- 💧 **Water Shortage**: Water purification and conservation
- 🩹 **Bleeding**: Wound care and bleeding control

### Search Tips
- Use specific keywords for better results
- Try multiple related terms
- Browse by emergency type using the sidebar
- Click on results to view detailed content

## Project Structure

```
signal-vault/
├── app.py                 # Main Flask application
├── main.py               # Command-line interface
├── requirements.txt      # Python dependencies
├── index_cache.pkl       # Pre-built search index
├── data/                 # Emergency documents (PDFs)
├── templates/            # HTML templates
├── index/               # Search engine modules
├── utils/               # Utility functions
└── signalvault-frontend/ # React frontend (optional)
```

## Dependencies

### Core Dependencies
- **Flask 3.1.1** - Web framework
- **pdfminer.six** - PDF text extraction
- **nltk 3.9.1** - Natural language processing
- **flask-cors 6.0.1** - Cross-origin resource sharing

### Full Dependencies List
```
blinker==1.9.0
cffi==1.17.1
charset-normalizer==3.4.2
click==8.1.8
cryptography==45.0.5
Flask==3.1.1
flask-cors==6.0.1
importlib_metadata==8.7.0
itsdangerous==2.2.0
Jinja2==3.1.6
joblib==1.5.1
MarkupSafe==3.0.2
nltk==3.9.1
pdfminer.six==20250506
pycparser==2.22
regex==2024.11.6
tqdm==4.67.1
Werkzeug==3.1.3
zipp==3.23.0
```

## Development

### Running in Development Mode
```bash
# Activate virtual environment
source .venv/bin/activate

# Run with debug mode
python app.py
```

### Building Search Index
The search index is pre-built and cached in `index_cache.pkl`. To rebuild:
```bash
# Delete existing cache
rm index_cache.pkl

# Run the application (will rebuild index)
python app.py
```

## Troubleshooting

### Common Issues

1. **Python Version Error**
   ```bash
   # Check Python version
   python --version
   # Should be 3.9+
   ```

2. **Module Not Found**
   ```bash
   # Ensure virtual environment is activated
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Port Already in Use**
   ```bash
   # Use a different port
   python app.py --port 5001
   ```

4. **PDF Processing Issues**
   - Ensure all PDF files are in the `data/` directory
   - Check file permissions
   - Try rebuilding the index

### Getting Help
- Check the [Issues](https://github.com/guneettt/signal-vault/issues) page
- Create a new issue with detailed error information
- Include your Python version and operating system

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Emergency documents sourced from various public safety organizations
- Built for emergency preparedness and offline access
- Designed with accessibility and usability in mind
