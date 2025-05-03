# README.md

# LlamaIndex Agent for Web Data Collection, Summarization, and Visualization

This project demonstrates how to develop an intelligent agent using LlamaIndex that interacts with MCP servers for advanced tools like Playwright. The agent performs web data collection, summarizes the content, and visualizes the results. The implementation showcases the use of multiple Python functions and methods, including data structures and library operations, to solve a complex problem.

## Features

- Web scraping and data extraction using Playwright and BeautifulSoup
- Data storage and manipulation with pandas
- Summarization of collected data
- Visualization of insights with matplotlib
- Interaction with MCP servers for advanced tool execution

## Requirements

Ensure you have the required libraries installed:

- llama_index
- mcp_client
- playwright
- beautifulsoup4
- matplotlib
- pandas

You can install the dependencies using:

```bash
pip install -r requirements.txt
```

## Files

- `main.py`: Main script implementing the agent logic
- `requirements.txt`: List of required Python libraries
- `README.md`: This documentation

## Usage

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the main script:

```bash
python main.py
```

## Notes

- Make sure to have Playwright browsers installed:

```bash
python -m playwright install
```

- Configure MCP server connection details as needed within the code.

---

# main.py

import asyncio
from typing import List, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
from llama_index import GPTIndex, SimpleKeywordTableIndex
from mcp_client import MCPClient
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

def initialize_mcp_client(server_url: str) -> MCPClient:
    """
    Initialize MCP client for server interaction.
    
    Args:
        server_url (str): URL of the MCP server.
        
    Returns:
        MCPClient: Initialized MCP client instance.
    """
    try:
        client = MCPClient(server_url)
        return client
    except Exception as e:
        print(f"Error initializing MCP client: {e}")
        raise

async def fetch_webpage(url: str, playwright) -> str:
    """
    Fetch webpage content asynchronously using Playwright.
    
    Args:
        url (str): URL of the webpage to fetch.
        playwright: Playwright instance.
        
    Returns:
        str: HTML content of the page.
    """
    try:
        browser = await playwright.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()
        return content
    except Exception as e:
        print(f"Error fetching webpage {url}: {e}")
        return ""

def parse_html(html_content: str) -> str:
    """
    Parse HTML content to extract text using BeautifulSoup.
    
    Args:
        html_content (str): Raw HTML content.
        
    Returns:
        str: Extracted text content.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return ""

def store_data_in_dataframe(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    Store list of data dictionaries into a pandas DataFrame.
    
    Args:
        data (List[Dict[str, Any]]): List of data entries.
        
    Returns:
        pd.DataFrame: DataFrame containing the data.
    """
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        return pd.DataFrame()

def summarize_text(texts: List[str]) -> str:
    """
    Generate a summary of multiple texts.
    
    Args:
        texts (List[str]): List of text strings to summarize.
        
    Returns:
        str: Summary of the combined texts.
    """
    combined_text = ' '.join(texts)
    # Placeholder for actual summarization logic, e.g., using GPT or other models
    summary = combined_text[:500] + '...' if len(combined_text) > 500 else combined_text
    return summary

def visualize_data(df: pd.DataFrame, column: str) -> None:
    """
    Create a bar plot for a specified column in the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame containing data.
        column (str): Column name to visualize.
    """
    try:
        counts = df[column].value_counts()
        counts.plot(kind='bar')
        plt.xlabel(column)
        plt.ylabel('Count')
        plt.title(f'Distribution of {column}')
        plt.show()
    except Exception as e:
        print(f"Error visualizing data: {e}")

async def main():
    """
    Main function to orchestrate web data collection, processing, and visualization.
    """
    server_url = "http://your-mcp-server.com"
    mcp_client = initialize_mcp_client(server_url)
    
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ]
    
    collected_texts = []
    data_entries = []
    
    async with async_playwright() as playwright:
        for url in urls:
            html_content = await fetch_webpage(url, playwright)
            text = parse_html(html_content)
            collected_texts.append(text)
            data_entries.append({"url": url, "content": text})
    
    df = store_data_in_dataframe(data_entries)
    summary = summarize_text(collected_texts)
    print("Summary of collected data:\n", summary)
    
    # Save DataFrame to CSV
    df.to_csv("collected_data.csv", index=False)
    
    # Visualize data (e.g., distribution of content length)
    df['content_length'] = df['content'].apply(len)
    visualize_data(df, 'content_length')

if __name__ == "__main__":
    asyncio.run(main())

# requirements.txt

llama_index
mcp_client
playwright
beautifulsoup4
matplotlib
pandas