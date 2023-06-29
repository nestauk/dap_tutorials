# An introduction to Web Scraping with Python

This have-a-go session will start with an theoretical introduction to **web scraping** followed by a practical tutorial on how to use [requests](https://pypi.org/project/requests/) and [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) Python packages for web scraping.

The agenda for the session is:
- Web scraping vs. web crawling
- Web scraping: use cases
- Legality and Ethics of Web scraping
- UK Exceptions to Copyright
- Denial of Service
- Terms of Service
- Robots Exclusion Protocol
- Web scraping: best practices
- Web scraping policies: public good institutions
- Python packages used for web scraping
- Have-a-go with requests and BeautifulSoup


## 🛠️ To do *before* the have-a-go session
Please follow the instructions below prior to the have-a-go session.

Open your terminal and follow the instructions. Shouldn't take longer than 5 minutes:
1. **Clone this repo:** 

`git clone https://github.com/nestauk/dap_tutorials.git`

2. **Navigate to this tutorial's folder:** 
Navigate to your repos folder (the folder where you store all your local GitHub repositories) and then do:

`cd dap_tutorials/intro_web_scraping/`

3. **Create your conda environment:** 

`conda create --name intro_web_scraping python=3.9`

4. **Activate your conda environment:** 

`conda activate intro_web_scraping`

5. **Install package dependencies:** 

`pip install -r requirements.txt`

6. **Add your conda environment to the notebooks:** 

`python -m ipykernel install --user --name=intro_web_scraping`

7. **Open the first notebook and make sure you have the correct kernel selected** 

Launch `jupyter-notebook` and open notebook `01. Scraping a news article.ipynb` and make sure your kernel is the right environment, `intro_web_scraping`. Run the notebooks to check if the previous setup worked for you. If all runs fine, then you're prepared for the session!

(If you do not have conda installed/do not want to install it, just use your standard Python environment