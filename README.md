# TrustNet360

TrustNet360 is a Python-based tool designed for comprehensive IP address analysis, aiding in cybersecurity threat detection and incident response. The tool leverages web scraping and automation techniques to provide features such as bulk IP lookup, integration with VirusTotal for enhanced threat intelligence, automated reporting, and extraction of geographical information.

## Features

- **Bulk IP Lookup:** Query multiple online services simultaneously for IP address analysis.
- **VirusTotal Integration:** Enhance threat intelligence by integrating with VirusTotal.
- **Automated Reporting:** Generate PDF and CSV reports for easy analysis and sharing.
- **Geographical Information Extraction:** Extract location details using pyppeteer and pycountry_convert libraries.
- **Screenshot Capture:** Capture screenshots for evidence and visualization of results.

## Technologies Used

- Python
- Selenium
- BeautifulSoup
- pyppeteer
- pycountry_convert
- argparse
- CSV handling

## Getting Started

1. Clone the repository:

    ```bash
    git clone https://github.com/trilokisingh/TrustNet360.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the tool:

    ```bash
    python TrustNet360.py <input_file.txt>
    ```

4. Optionally, enable VirusTotal integration for screenshots:

    ```bash
    python TrustNet360.py <input_file.txt> -vt
    ```

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvement, please submit an issue or open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the developers of pycountry-convert and VirusTotal for their APIs.

Feel free to adjust the content as needed and include any additional sections or information relevant to your project.
