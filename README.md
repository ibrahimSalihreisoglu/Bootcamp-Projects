# Bootcamp-Projects

## Genel Bakış
Bu repo, bootcamp sürecinde geliştirdiğim projeleri içerir.  
Her projede uçtan uca süreci (veri hazırlama, analiz, modelleme/değerlendirme ve çıkarımlar) dokümante ediyorum.

## Projeler

### 1) Amazon Yorum Puanlama & Yorum Sıralama
- Amaç: Ürün puanını zaman ağırlıklı hesaplamak ve yorumları en güvenilir şekilde sıralamak.
- Adımlar:
  - Average Rating ile Time-Weighted Rating karşılaştırması
  - `helpful_no` değişkeninin oluşturulması
  - `score_pos_neg_diff`, `score_average_rating` ve `wilson_lower_bound` hesaplanması
  - WLB skoruna göre Top 20 yorumun seçilmesi
- Dosyalar:
  - `amazon_review_project.py`
  - `amazon_review.csv`

### 2) A/B Testing: Bidding Yöntemlerinin Dönüşüm Karşılaştırması
- Amaç: Maximum Bidding (Control) ve Average Bidding (Test) yöntemlerinin Purchase (satın alma) ortalamalarını karşılaştırıp istatistiksel olarak anlamlı fark var mı görmek.
- Adımlar:
  - Veri okuma (Excel: Control Group / Test Group)
  - Keşifsel analiz (özet istatistikler, ortalamalar)
  - Varsayım kontrolleri: Normallik (Shapiro), Varyans homojenliği (Levene)
  - Uygun test seçimi: Student t-test / Welch t-test / Mann-Whitney U
  - p-value’a göre sonuç yorumu ve öneri
- Dosyalar:
  - `AB_TESTING.py`
  - `ab_testing.xlsx`
