import pandas as pd, time, re, requests
from bs4 import BeautifulSoup
from googlesearch import search
from io import BytesIO

def run_contact_extraction(file_content):
    df = pd.read_excel(BytesIO(file_content))
    company_column = df.columns[0]
    df['Website'] = ''
    df['Emails'] = ''
    df['Phones'] = ''

    for i, company in enumerate(df[company_column]):
        try:
            query = f"{company} official site"
            url = next(search(query, num=1, stop=1, pause=2), None)
            df.at[i, 'Website'] = url if url else 'Not Found'

            if url:
                headers = {'User-Agent': 'Mozilla/5.0'}
                resp = requests.get(url, headers=headers, timeout=5)
                text = BeautifulSoup(resp.text, 'html.parser').get_text()
                emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
                phones = re.findall(r'\+?\d{1,4}?[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}', text)
                df.at[i, 'Emails'] = ', '.join(set(emails))
                df.at[i, 'Phones'] = ', '.join(set(phones))

            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Error on row {i+1}: {e}")

    return df
