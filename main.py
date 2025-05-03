# main.py

import asyncio
from typing import List, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
from llama_index import GPTIndex, SimpleKeywordTableIndex, ServiceContext
from mcp_client import MCPClient
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

def fetch_webpage_content(url: str, playwright_instance) -> str:
    """
    Fetches the HTML content of a webpage using Playwright.
    Args:
        url (str): The URL of the webpage to fetch.
        playwright_instance: The Playwright instance.
    Returns:
        str: The HTML content of the page.
    """
    try:
        browser = await playwright_instance.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()
        return content
    except Exception as e:
        print(f"Error fetching webpage {url}: {e}")
        return ""

def parse_html_for_data(html_content: str) -> List[Dict[str, Any]]:
    """
    Parses HTML content to extract data items.
    Args:
        html_content (str): The HTML content to parse.
    Returns:
        List[Dict[str, Any]]: Extracted data items.
    """
    data_items = []
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        # Example: extract all links with their text
        for link in soup.find_all('a', href=True):
            data_items.append({'text': link.get_text(), 'href': link['href']})
    except Exception as e:
        print(f"Error parsing HTML: {e}")
    return data_items

def summarize_data(data: List[Dict[str, Any]]) -> str:
    """
    Summarizes the collected data into a textual report.
    Args:
        data (List[Dict[str, Any]]): The data items to summarize.
    Returns:
        str: The summary text.
    """
    try:
        df = pd.DataFrame(data)
        summary = f"Collected {len(df)} links.\n"
        top_domains = df['href'].apply(lambda x: x.split('/')[2] if '//' in x else 'N/A')
        domain_counts = top_domains.value_counts().head(5)
        summary += "Top 5 domains:\n"
        for domain, count in domain_counts.items():
            summary += f"{domain}: {count}\n"
        return summary
    except Exception as e:
        print(f"Error summarizing data: {e}")
        return "Summary could not be generated."

def visualize_data(data: List[Dict[str, Any]]) -> None:
    """
    Creates a bar chart of the top domains in the data.
    Args:
        data (List[Dict[str, Any]]): The data items to visualize.
    """
    try:
        df = pd.DataFrame(data)
        top_domains = df['href'].apply(lambda x: x.split('/')[2] if '//' in x else 'N/A')
        domain_counts = top_domains.value_counts().head(10)
        domain_counts.plot(kind='bar')
        plt.title('Top 10 Domains')
        plt.xlabel('Domain')
        plt.ylabel('Number of Links')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print(f"Error visualizing data: {e}")

async def main():
    """
    Main function to orchestrate web data collection, summarization, and visualization.
    """
    # Initialize MCP client for advanced tools
    mcp = MCPClient()
    # Example: Use MCP to run Playwright for web scraping
    async with async_playwright() as playwright:
        url = "https://example.com"
        html_content = await fetch_webpage_content(url, playwright)
        if not html_content:
            print("Failed to fetch webpage content.")
            return
        data_items = parse_html_for_data(html_content)
        if not data_items:
            print("No data extracted from webpage.")
            return
        summary = summarize_data(data_items)
        print("Data Summary:\n", summary)
        visualize_data(data_items)

if __name__ == "__main__":
    asyncio.run(main())

# requirements.txt

llama_index
mcp_client
playwright
beautifulsoup4
matplotlib
pandas

# README.md

# Web Data Collector and Visualizer using LlamaIndex and MCP

This script fetches webpage data using Playwright, extracts links with BeautifulSoup, summarizes the data, and visualizes the top domains. It demonstrates modular Python functions, interaction with MCP servers for advanced tools, and data processing techniques.