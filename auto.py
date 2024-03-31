import streamlit as st
import fitz  # PyMuPDF
import os
from openai import OpenAI
client = OpenAI(api_key=st.secrets['api_key'])
st.set_page_config(
    page_title="HUBX",
    page_icon="./logo.ico  ",
)
st.markdown(
    f'<img src="https://evalian.co.uk/wp-content/uploads/2022/06/logo.png" style="max-width:25%; background-color:white; height:auto;">', 
    unsafe_allow_html=True
)
def read_pdf(file):
    text = ""
    pdf_document = fitz.open(stream=file.getvalue(), filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += f"### Page {page_num + 1}\n"  # Add page number as heading
        text += page.get_text()
    system = """
    This is a pitch deck transcript. Give a Page By Page Review of the entire transcript. Suggest possible improvements and suggestions. A good pitch deck is essential for effectively communicating your business idea, product, or service to potential investors, partners, or customers.
    Whenever possible Give Suggestive Content Replacements marking content that can be replaced with something more impactive. Give industry relevant feedback. 

    It should contain these details: 
    Cover Slide: The cover slide should include your company's name, logo, and a tagline or brief description that encapsulates your value proposition.

    Problem Statement: Clearly articulate the problem or pain point that your product or service addresses. Explain why this problem is significant and how it impacts your target market.

    Solution: Present your solution to the problem. Describe your product or service and how it effectively solves the problem identified. Highlight the key features and benefits that differentiate your solution from existing alternatives.

    Market Opportunity: Provide an overview of the market opportunity. Define your target market, including its size, demographics, and any relevant trends or growth opportunities. Explain how your solution meets the needs of this market.

    Business Model: Outline your business model and how you plan to generate revenue. Describe your pricing strategy, sales channels, and any partnerships or collaborations that support your revenue generation.

    Traction: Share any traction or validation that your product or service has achieved. This may include customer testimonials, user metrics, revenue numbers, or partnerships with key clients or stakeholders.

    Go-to-Market Strategy: Detail your go-to-market strategy for acquiring customers or users. Explain how you plan to reach your target audience, acquire customers, and drive adoption of your product or service.

    Marketing and Sales Strategy: Outline your marketing and sales strategy for promoting your product or service. Describe the channels, tactics, and campaigns you will use to attract customers and drive sales.

    Team: Introduce your team members and their relevant expertise. Highlight any previous experience, skills, or achievements that demonstrate their ability to execute on the business idea.

    Financial Projections: Present financial projections for your business, including revenue forecasts, expense estimates, and projected growth metrics. Provide a clear understanding of the financial potential of your business.

    Funding Needs: Clearly state the amount of funding you are seeking and how you plan to use it. Break down the funding requirements and explain how the investment will fuel the growth and success of your business.

    Appendix: Include any additional information or supporting materials that provide context or validation for your pitch. This may include product demos, market research data, customer testimonials, or competitive analysis.
    
    """
    completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=1,
            presence_penalty=-1,
            messages=[{"role":"system","content":system},{"role":"user","content":text}]
    )

    return completion.choices[0].message.content
def main():

    st.title("PDF Pitch Extractor")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        st.write("### Transcribed Text:")
        text = read_pdf(uploaded_file)
        st.markdown(text, unsafe_allow_html=True)  # Allow HTML to render headings

if __name__ == "__main__":
    main()
