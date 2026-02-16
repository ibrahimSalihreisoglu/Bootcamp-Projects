import pandas as pd
import math
df = pd.read_csv("/workspaces/Bootcamp-Projects/amazon_review.csv")
#Görev 1:  AverageRating’igüncel yorumlara göre hesaplayınız ve var olan averageratingile kıyaslayınız.

average_rating = df["overall"].mean()

def tarihe_göre_puan_ağırlıklı(data, w1=0.28, w2=0.26, w3=0.24, w4=0.22):
 return(
    df.loc[df["day_diff"]<30,"overall"].mean()*w1+
    df.loc[(df["day_diff"]>30)&(df["day_diff"]<60),"overall"].mean()*w2+
    df.loc[(df["day_diff"]>60)&(df["day_diff"]<90),"overall"].mean()*w3+
    df.loc[df["day_diff"]>90,"overall"].mean()*w4
)
weighted_rating= tarihe_göre_puan_ağırlıklı(df)
comparison = pd.DataFrame({
    "metric": ["Average Rating (tüm yorumlar)", "Time-Weighted Rating (güncel ağırlıklı)"],
    "value": [average_rating, weighted_rating]
})
comparison["difference"] = comparison["value"] - average_rating
comparison

#Görev 2:  Ürün için ürün detay sayfasında görüntülenecek 20 review’ibelirleyiniz
df["helpful_no"]=df["total_vote"]-df["helpful_yes"]

def score_pos_neg_diff(up, down):
    return up - down

df["score_pos_neg_diff"] = df.apply(
    lambda x: score_pos_neg_diff(x["helpful_yes"], x["helpful_no"]),
    axis=1)


def score_average_rating(up, down):
    total = up + down
    return 0 if total == 0 else up / total

df["score_average_rating"] = df.apply(
    lambda x: score_average_rating(x["helpful_yes"], x["helpful_no"]),
    axis=1)


def wilson_lower_bound(up, down, confidence=0.95):
    n = up + down
    if n == 0:
        return 0

    z = 1.959963984540054  
    phat = up / n

    return (phat + z*z/(2*n) - z*math.sqrt((phat*(1-phat) + z*z/(4*n))/n)) / (1 + z*z/n)

df["wilson_lower_bound"] = df.apply(
    lambda x: wilson_lower_bound(x["helpful_yes"], x["helpful_no"]),
    axis=1)

top20 = df.sort_values("wilson_lower_bound", ascending=False).head(20)

top20[[
    "reviewTime", "day_diff", "overall",
    "helpful_yes", "helpful_no", "total_vote",
    "score_pos_neg_diff", "score_average_rating", "wilson_lower_bound",
    "summary", "reviewText"
]]
print("Average Rating:", average_rating)
print("\nKarşılaştırma:")
print(comparison)

# Top 20 yorumu yazdırmak için (WLB varsa)
top20 = df.sort_values("wilson_lower_bound", ascending=False).head(20)
print("\nTop 20 (WLB):")
print(top20[["overall","helpful_yes","helpful_no","wilson_lower_bound","summary"]].to_string(index=False))
