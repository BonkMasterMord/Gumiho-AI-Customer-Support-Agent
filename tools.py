from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

def save_to_txt(data: str, filename: str = "Response_Output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Agent Response Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

# Define FAQ for Gumiho LLC
company_faq = {
    "what is gumiho llc": "Gumiho LLC is a Ginseng company specializing in delievering High Quality Ginseng.",
    "shipping": "If you are a business owner in North New Jersey, we directly deliver to you without shipping fees, but signature is required upon completion of delivery. For all others, We use postal services such as UPS or FedEx, and negotiable delivery fees may be applied ",
    "return policy": "Returns are accepted within 14 days of purchase for unopened, unused products in their original packaging. Defective, damaged, or incorrect items must be reported within 3 days, as we cannot accept returns for defects reported after the specified timeframe. Products damaged due to misuse, mishandling, or improper storage by the buyer are not eligible for return or refund. Custom or special-order products are non-returnable. A 15% restocking fee will be applied to the cost of each non-defective returned product 3 days after completion of delivery. Outstanding unpaid balances will incur an additional charge of 1.5% per month until fully paid. To initiate a return, contact us with the information above with your invoice number. Return shipping costs are the buyer's responsibility unless the issue is our error. Refunds will be processed after inspection. By signing below, you agree to these terms.",
    "contact": "Email services@gumihollc.com or call (201)-916-4295.",
    "delivery time": "Orders ship Monday through Saturday with the exception of national holidays. Orders with expedited delivery must reach us before 2 p.m. (Eastern Standard Time) to ship same day. However, individual shipments may take up to 3 to business days."
}

# Function to look up company information based on user query
def company_info_lookup(question: str):
    question = question.lower()
    for k, v in company_faq.items():
        if k in question:
            return v
    return "Sorry, I couldn't find information about that."

from langchain.tools import Tool

company_info_tool = Tool(
    name="company_info_faq",
    func=company_info_lookup,
    description="Get information about Gumiho LLC's company policies, products, and contact info."
)


# Save tool to save responses into a text file
save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

# Search tool to search the web for information
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
