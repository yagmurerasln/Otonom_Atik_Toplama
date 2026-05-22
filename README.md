# Otonom Atık Toplama ve Rota Optimizasyonu

Bu proje, **Pekiştirmeli Öğrenme Dönem Sonu Projesi** kapsamında geliştirilecektir.  
Amaç, akıllı şehir ortamında otonom bir atık toplama aracının, konteyner doluluk oranlarına göre en uygun rotayı öğrenmesini ve atık toplama sürecini optimize etmesini sağlamaktır.

## Proje Konusu

Akıllı şehirlerde atık yönetimi, zaman, maliyet, enerji tüketimi ve çevresel etkiler açısından önemli bir problemdir. Geleneksel atık toplama yöntemlerinde araçlar genellikle sabit rotaları takip eder. Ancak bu yaklaşım, bazı konteynerler boşken gereksiz ziyaretlere, bazıları doluyken ise gecikmelere neden olabilir.

Bu projede, konteyner doluluk oranları dikkate alınarak bir atık toplama aracının hangi noktaya gideceğini öğrenmesi hedeflenmektedir. Araç, pekiştirmeli öğrenme yöntemiyle çevreden aldığı ödül ve cezalar doğrultusunda daha verimli rotalar oluşturmayı öğrenecektir.

## Amaç

Projenin temel amacı:

- Akıllı şehir ortamını basit bir simülasyon olarak modellemek
- Atık konteynerlerinin doluluk oranlarını sisteme dahil etmek
- Otonom atık toplama aracının hareketlerini simüle etmek
- Pekiştirmeli öğrenme ile rota kararlarını optimize etmek
- Pygame kullanarak süreci görselleştirmek

## Kullanılacak Teknolojiler

- Python
- Pygame
- NumPy
- Matplotlib
- Q-Learning
- Reinforcement Learning temel kavramları

## Proje Ortamı

Başlangıç aşamasında şehir ortamı 2 boyutlu bir grid yapısı olarak modellenir.

Örnek ortam:

- 10x10 şehir haritası
- 1 adet atık toplama aracı
- Birden fazla atık konteyneri
- Konteyner doluluk oranları
- Depo / başlangıç noktası
- Hareket ve rota takibi

## Pekiştirmeli Öğrenme Modeli

Bu projede atık toplama aracı bir **ajan** olarak tanımlanır.

### Agent

Atık toplama aracı.

### Environment

Akıllı şehir grid ortamı.

### State

Ajanın bulunduğu konum, konteynerlerin doluluk durumu ve çevre bilgileri.

### Action

Ajanın yapabileceği hareketler:

- Yukarı git
- Aşağı git
- Sola git
- Sağa git

### Reward

Ajanın davranışlarına göre ödül veya ceza verilir.

Örnek reward mantığı:

- Her hareket için küçük ceza
- Dolu konteyner toplandığında ödül
- Gereksiz hareketlerde ceza
- Tüm gerekli konteynerler toplandığında yüksek ödül
- Depoya dönüldüğünde ek ödül

## Görselleştirme

Proje Pygame ile görselleştirilecektir.

Görselleştirmede yer alacak öğeler:

- Şehir grid haritası
- Atık toplama aracı
- Atık konteynerleri
- Konteyner doluluk oranları
- Depo noktası
- Aracın izlediği rota
- Toplam ödül / skor bilgisi

## Basit Proje Akışı

1. Şehir grid ortamı oluşturulur.
2. Konteynerlerin konumları ve doluluk oranları belirlenir.
3. Atık toplama aracı başlangıç noktasına yerleştirilir.
4. Araç hareket kurallarına göre ortamda ilerler.
5. Reward sistemi tanımlanır.
6. Q-Learning algoritması ile ajan eğitilir.
7. Elde edilen rota Pygame ile görselleştirilir.
8. Sonuçlar analiz edilir.

## Önerilen Dosya Yapısı

```text
otonom-atik-toplama-rl/
│
├── main.py
├── environment.py
├── agent.py
├── baseline.py
├── visualization.py
├── requirements.txt
├── README.md
│
├── results/
│   ├── reward_plot.png
│   └── route_plot.png
│
└── report/
    └── proje_raporu.pdf
```

## Kurulum

Projeyi klonladıktan sonra gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

Eğer `requirements.txt` henüz oluşturulmadıysa temel kurulum için:

```bash
pip install pygame numpy matplotlib
```

## Çalıştırma

Ana dosyayı çalıştırmak için:

```bash
python main.py
```

## Beklenen Çıktılar

Proje sonunda aşağıdaki çıktılar hedeflenmektedir:

- Çalışan bir şehir simülasyonu
- Pygame ile görselleştirilmiş atık toplama rotası
- Q-Learning ile eğitilmiş basit bir ajan
- Baseline algoritma ile karşılaştırma
- Toplam mesafe, toplanan konteyner sayısı ve ödül değerleri
- Proje raporu ve sonuç analizi

## Gelecekte Eklenebilecek Özellikler

- Gerçek harita verisi kullanımı
- OpenStreetMap entegrasyonu
- Trafik yoğunluğu
- Araç kapasitesi
- Çoklu atık toplama aracı
- Dinamik konteyner doluluk oranları
- DQN veya PPO gibi gelişmiş RL algoritmaları
- Karbon emisyonu optimizasyonu

## Proje Durumu

Proje geliştirme aşamasındadır.

## Lisans

Bu proje eğitim amacıyla geliştirilmektedir.
