import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

# URL utama daftar skripsi
url = 'https://repository.its.ac.id/view/subjects/T57=2E8.html'
base_url = 'https://repository.its.ac.id'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'  # Biar gak gampang ditolak server
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

# Simpan hasil
data = []



# Cari semua link
for a_tag in soup.find_all('a', href=True):
    href = a_tag.get('href')
    em_tag = a_tag.find('em')

    if not em_tag:
        continue  # Hanya proses link yang ada <em> (berarti link ke judul)

    if href.startswith('/'):
        link = base_url + href
    elif href.startswith('http'):
        link = href
    else:
        continue  # Skip kalau href aneh

    title = em_tag.text.strip()  # Ambil text dari <em>

    # Masuk ke halaman detail
    try:
        detail_response = requests.get(link, headers=headers)
        detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

        # Ambil penulis
        author_tag = detail_soup.find('span', class_='person_name')
        author = author_tag.text.strip() if author_tag else 'Tidak ditemukan'

        # Ambil abstrak
        abstract_tag = detail_soup.find('p', class_='ep_field_para')
        abstract = abstract_tag.text.strip() if abstract_tag else 'Tidak ditemukan'

        # Simpan hasil
        data.append({
            'Judul': title,
            'Link': link,
            'Penulis': author,
            'Abstrak': abstract
        })

        print(f"Sukses ambil: {title}")  # Status biar kelihatan progres

        time.sleep(1)  # Delay biar aman

    except Exception as e:
        print(f"Error saat ambil detail {link}: {e}")
        continue

df = pd.DataFrame(data)

# Simpan ke CSV
df.to_csv('hasil_scraping_skripsi.csv', index=False, columns=['Judul', 'Penulis', 'Link', 'Abstrak'])
df = df[['Judul', 'Penulis', 'Link', 'Abstrak']]

print("✅ Data berhasil disimpan ke 'hasil_scraping_skripsi.csv'!")
# Cetak hasil
for item in data:
    print(f"Judul: {item['Judul']}")
    print(f"Link: {item['Link']}")
    print(f"Penulis: {item['Penulis']}")
    print(f"Abstrak: {item['Abstrak']}")
    print('---')
