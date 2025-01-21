GNews Summarization
Pembuat: Galih Putra Pratama

GNews Summarization adalah sebuah aplikasi yang menggabungkan teknologi pemrosesan bahasa alami dan machine learning untuk merangkum artikel berita secara otomatis. 
Proyek ini berfokus pada membantu pengguna mendapatkan informasi yang relevan dari artikel berita tanpa terganggu oleh iklan atau elemen yang tidak penting. 
Selain itu, aplikasi ini juga menghasilkan hashtag yang relevan berdasarkan artikel tersebut.

Latar Belakang:
Sering kali, ketika seseorang membaca artikel berita di internet, mereka dihadapkan pada berbagai gangguan seperti iklan yang muncul tiba-tiba atau artikel yang terlalu panjang dan bertele-tele. 
Hal ini mengurangi kenyamanan pembaca dan memperlambat pemahaman informasi. Oleh karena itu, GNews Summarization hadir untuk memberikan solusi dengan merangkum artikel secara efisien dan menyingkirkan gangguan tersebut.

NOTES : untuk hasil summary article akan otomatis dibuat di path ini D:\KULIAH\SEMESTER 5\STKI\GNews_Summarization\news_summaries.xlsx  , maka pengguna tidak perlu membuat folder secar amanual

Metode yang Digunakan dalam Proyek:
GNews Summarization menggunakan berbagai metode dan teknik untuk memproses dan merangkum artikel. Berikut adalah detail dari metode yang digunakan:
1. Pengambilan Artikel (Web Scraping):
    Teknik yang digunakan: requests, BeautifulSoup
    Deskripsi: Artikel diambil melalui URL yang diberikan pengguna menggunakan requests untuk mengunduh HTML halaman. Kemudian, BeautifulSoup digunakan untuk mem-parsing HTML dan mengekstrak teks artikel, mengabaikan elemen-elemen yang tidak relevan seperti iklan atau sidebar.
2. Penerjemahan Artikel (Opsional):
    Teknik yang digunakan: googletrans API (Google Translate)
    Deskripsi: Artikel yang diambil dapat diterjemahkan ke dalam bahasa yang dipilih oleh pengguna menggunakan API googletrans. Jika artikel sudah dalam bahasa yang dipilih, maka artikel tidak diterjemahkan lagi.
3. Pembuatan Ringkasan Artikel:
    GNews Summarization menawarkan dua metode untuk merangkum artikel:
    a. Ringkasan Fleksibel (Clustering):
        Teknik yang digunakan: KMeans Clustering, TF-IDF (Term Frequency-Inverse Document Frequency)
        Deskripsi:
        Artikel dibagi menjadi beberapa klaster menggunakan algoritma KMeans yang dikoordinasi dengan representasi teks berbasis TF-IDF. Teknik ini mengukur pentingnya setiap kata dalam artikel berdasarkan frekuensinya (TF) dan betapa jarangnya kata tersebut dalam seluruh korpus (IDF).
        Setiap klaster berisi kalimat-kalimat yang serupa dalam topik, dan kalimat-kalimat utama dari setiap klaster diambil untuk membentuk ringkasan yang lebih terfokus.
    b. Ringkasan Panjang (Long Summary):
        Teknik yang digunakan: Penyusunan kalimat secara langsung
        Deskripsi:
        Ringkasan ini dihasilkan dengan menggabungkan seluruh kalimat dalam artikel secara langsung untuk menghasilkan satu paragraf panjang yang menggambarkan keseluruhan artikel.
        Ini lebih cocok untuk memberikan gambaran umum daripada ringkasan yang sangat singkat.

4. Pembuatan Hashtag:
    Teknik yang digunakan: TF-IDF untuk memilih kata-kata yang paling relevan
    Deskripsi:
    Sistem menganalisis judul dan konten artikel untuk menghasilkan hashtag yang relevan. Dengan menggunakan teknik TF-IDF, sistem memilih kata-kata yang paling sering muncul dan penting dalam artikel.
    Hashtag ini membantu pengguna memahami topik utama dari artikel dan mempermudah pencarian artikel dengan topik serupa di media sosial atau platform lain.
5. Penyimpanan dan Pengelolaan Data:
    Teknik yang digunakan: Pandas (untuk pengelolaan data), Excel (untuk penyimpanan)
    Deskripsi:
    Semua ringkasan dan hashtag yang dihasilkan disimpan dalam file Excel (news_summaries.xlsx). File ini berfungsi sebagai database yang berisi hasil ringkasan yang bisa dimuat kembali untuk dianalisis atau dilihat kembali oleh pengguna.

Antarmuka Pengguna (Streamlit): Streamlit digunakan untuk membuat antarmuka pengguna. Pengguna dapat memasukkan URL artikel, memilih bahasa, dan melihat hasil ringkasan serta hashtag yang dihasilkan. Data yang dihasilkan juga dapat disimpan dan dilihat dalam bentuk tabel.
Visualisasi: Infografis berupa visualisasi jumlah kata per titik ringkasan ditampilkan dengan menggunakan matplotlib, memberikan gambaran yang lebih jelas tentang struktur ringkasan.

Langkah-langkah Penggunaannya:
1. Input URL Artikel: Pengguna memasukkan URL artikel yang ingin dianalisis.
2. Pilih Bahasa: Pengguna memilih bahasa untuk terjemahan artikel (jika diperlukan).
3. Proses Ringkasan: Pengguna menekan tombol "Summarize and Generate Hashtags" untuk memulai proses pembuatan ringkasan dan hashtag.
4. Lihat Ringkasan dan Hashtag: Hasil ringkasan dan hashtag akan ditampilkan.
5. Simpan dan Lihat Dataset: Data ringkasan yang telah dihasilkan akan disimpan ke dalam file Excel dan dapat dilihat dalam aplikasi.

Penjelasan Kode:
Import Libraries: Kode ini menggunakan beberapa pustaka Python untuk melakukan pemrosesan teks, pembuatan aplikasi web, serta pengolahan data dan visualisasi. Beberapa pustaka yang digunakan antara lain:
1. nltk: Untuk pemrosesan teks seperti tokenisasi.
2. streamlit: Untuk membangun aplikasi web interaktif.
3. requests: Untuk mengambil data dari URL (untuk mengunduh artikel).
4. BeautifulSoup: Untuk mem-parsing HTML artikel.
5. matplotlib: Untuk visualisasi infografis.
6. sklearn: Untuk pemrosesan data dan klasterisasi.
7. googletrans: Untuk terjemahan teks.
8. pandas: Untuk manipulasi data (misalnya menyimpan dan memuat dataset).

Penjelasan Fungsi:
1. Fungsi save_to_excel: Fungsi ini menyimpan atau memperbarui dataset yang berisi ringkasan artikel dan tagar yang dihasilkan ke dalam file Excel. Jika file tidak ada, maka file baru akan dibuat.
2. Fungsi load_dataset: Fungsi ini digunakan untuk memuat dataset dari file Excel yang sudah ada. Ini memungkinkan Anda untuk melihat riwayat ringkasan yang sudah dihasilkan.
3. Stopwords untuk Berbagai Bahasa: Variabel stop_words berisi stopwords (kata-kata umum yang sering muncul dalam teks tetapi tidak memiliki makna penting) untuk berbagai bahasa, seperti bahasa Inggris, Indonesia, Spanyol, dan Prancis.
4. Fungsi fetch_article: Fungsi ini mengambil artikel dari URL yang diberikan. Fungsi ini akan mengambil judul dan isi artikel, serta membersihkan artikel dari iklan atau teks yang tidak relevan menggunakan pola regex.
5. Fungsi summarize_article_flexible: Fungsi ini menganalisis artikel dan menyarikan artikel tersebut menggunakan klasterisasi dengan algoritma KMeans berdasarkan TF-IDF. Artikel dibagi menjadi beberapa klaster dan kemudian diambil kalimat-kalimat kunci dari setiap klaster untuk membentuk ringkasan.
6. Fungsi long_summary: Fungsi ini menghasilkan ringkasan yang lebih panjang dengan menggabungkan seluruh kalimat dalam artikel.
7. Fungsi translate_article: Fungsi ini akan menterjemahkan artikel ke dalam bahasa yang dipilih pengguna. Jika artikel sudah dalam bahasa yang sama dengan yang dipilih, artikel tidak akan diterjemahkan lagi.
8. Fungsi generate_hashtags: Fungsi ini menganalisis judul dan isi artikel untuk menghasilkan hashtag yang relevan menggunakan teknik TF-IDF untuk menghitung kata-kata yang paling penting.
9. Fungsi main: Fungsi utama dari aplikasi Streamlit. Di sini pengguna dapat:
    a. Memasukkan URL artikel yang akan dianalisis.
    b. Memilih bahasa terjemahan.
    c. Mengklik tombol untuk memulai proses ringkasan dan pembuatan hashtag.
    d. Melihat hasil ringkasan dan tagar yang dihasilkan.
    e. Menyimpan hasil ke dalam dataset dan menampilkan dataset dalam antarmuka aplikasi.