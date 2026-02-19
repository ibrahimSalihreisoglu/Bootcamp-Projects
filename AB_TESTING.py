
# GÖREV 1: Veriyi Hazırlama ve Analiz Etme

# Adım 1: Excel dosyasını oku ve kontrol/test gruplarını ayır
file_path = "ab_testing_data.xlsx"  # dosya adı farklıysa değiştir
sheets = pd.read_excel(file_path, sheet_name=None)

control = sheets["Control Group"].copy()
test    = sheets["Test Group"].copy()

# Adım 2: Kontrol ve test grubunu analiz et (basit özet)
print("=== GÖREV 1 / Adım 2: Kısa Analiz ===")
print("Control shape:", control.shape)
print("Test shape   :", test.shape)
print("Control Purchase ort:", control["Purchase"].mean())
print("Test Purchase ort   :", test["Purchase"].mean())

# Adım 3: Concat ile kontrol ve test verisini birleştir
control["group"] = "control"
test["group"]    = "test"
df = pd.concat([control, test], ignore_index=True)

print("\n=== GÖREV 1 / Adım 3: Birleşmiş veri (ilk 5 satır) ===")
print(df.head())


# GÖREV 2: A/B Testinin Hipotezinin Tanımlanması


# Adım 1: Hipotezleri tanımla
# H0: M1 = M2  (Kontrol ve test grubunun Purchase ortalamaları eşittir)
# H1: M1 != M2 (Kontrol ve test grubunun Purchase ortalamaları eşit değildir)

# Adım 2: Kontrol ve test grubunun Purchase ortalamalarını kontrol et
print("\n=== GÖREV 2 / Adım 2: Purchase Ortalamaları ===")
control_mean = control["Purchase"].mean()
test_mean = test["Purchase"].mean()
print("Control mean (Purchase):", control_mean)
print("Test mean (Purchase)   :", test_mean)


# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi


alpha = 0.05
x = control["Purchase"]
y = test["Purchase"]

# Adım 1: Varsayım kontrolleri (Normallik + Varyans homojenliği)

# Normallik testi (Shapiro) - her grup için ayrı
# H0: Normal dağılım vardır
# H1: Normal dağılım yoktur
p_shapiro_control = stats.shapiro(x).pvalue
p_shapiro_test    = stats.shapiro(y).pvalue

# Varyans homojenliği (Levene)
# H0: Varyanslar eşittir (homojen)
# H1: Varyanslar eşit değildir
p_levene = stats.levene(x, y).pvalue

print("\n=== GÖREV 3 / Adım 1: Varsayım Testleri ===")
print("Shapiro p (control):", p_shapiro_control)
print("Shapiro p (test)   :", p_shapiro_test)
print("Levene p           :", p_levene)

# Adım 2: Varsayımlara göre uygun testi seç
normality_ok = (p_shapiro_control > alpha) and (p_shapiro_test > alpha)
variance_ok = (p_levene > alpha)

# - Normallik sağlanıyorsa -> t-test (varyans eşitse Student, değilse Welch)
# - Normallik sağlanmıyorsa -> Mann-Whitney U
if normality_ok:
    result = stats.ttest_ind(x, y, equal_var=variance_ok)

    if variance_ok:
        test_used = "Student t-test (varyanslar eşit)"
    else:
        test_used = "Welch t-test (varyanslar eşit değil)"

    p_value = result.pvalue
else:
    result = stats.mannwhitneyu(x, y, alternative="two-sided")
    test_used = "Mann-Whitney U (non-parametrik)"
    p_value = result.pvalue

# Adım 3: p-value ile anlamlı fark var mı yorumla
print("\n=== GÖREV 3 / Adım 3: Hipotez Testi Sonucu ===")
print("Kullanılan test:", test_used)
print("p-value:", p_value)

if p_value < alpha:
    print("SONUÇ: İstatistiksel olarak anlamlı fark VAR (H0 reddedilir).")
else:
    print("SONUÇ: İstatistiksel olarak anlamlı fark YOK (H0 reddedilemez).")


# GÖREV 4: Sonuçların Analizi

# Adım 1: Hangi testi kullandın, neden?
print("\n=== GÖREV 4 / Adım 1: Test Seçim Gerekçesi ===")
if normality_ok and variance_ok:
    print("Normallik sağlandı ve varyanslar homojen -> Student t-test kullanıldı.")
elif normality_ok and not variance_ok:
    print("Normallik sağlandı ama varyanslar homojen değil -> Welch t-test kullanıldı.")
else:
    print("Normallik sağlanmadı -> Mann-Whitney U kullanıldı.")

# Adım 2: Müşteriye tavsiye
print("\n=== GÖREV 4 / Adım 2: Tavsiye ===")
print("Control Purchase ort:", control_mean)
print("Test Purchase ort   :", test_mean)

if p_value < alpha:
    if test_mean > control_mean:
        print("Test grubu anlamlı şekilde daha iyi -> Average Bidding (B) yayına alınabilir.")
    else:
        print("Test grubu anlamlı şekilde daha kötü -> Maximum Bidding (A) ile devam edin.")
else:
    print("Anlamlı fark yok -> Şimdilik A ile devam; test süresini uzatıp tekrar deneyin.")
