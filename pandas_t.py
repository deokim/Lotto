import numpy as np
import pandas as pd

#s= pd.Series([1,3,5,np.nan, 7])

#print(s)

dates=pd.date_range("20130101", periods=6)
#print(dates)

df=pd.DataFrame(np.random.randn(6,4), index=dates, columns=["A", "B", "C", "D"])

df1=df.reindex(index=dates[0:4], columns=list(df.columns)+["E"])
df1.loc[dates[0]:dates[1], "E"]=1

s=df1.mean(axis=1)

s = pd.DataFrame(
        {   "A": ["foo", "bar", "foo", "bar", "foo", "bar", "foo", "foo"],
            "B": ["one", "one", "two", "three", "two", "two", "one", "three"],
            "C": np.random.randn(8),
            "D": np.random.randn(8),
        }
    )
    
t=s.groupby(["A", "B"]).sum()

## MultiIndex
arrays = [
   ["bar", "bar", "baz", "baz", "foo", "foo", "qux", "qux"],
   ["one", "two", "one", "two", "one", "two", "one", "two"],
]

index=pd.MultiIndex.from_arrays(arrays, names=["first","second"])
t=pd.DataFrame(np.random.randn(8,2), index=index, columns=list("AB"))

## Pivot Table
df = pd.DataFrame(
    {
        "A": ["one", "one", "two", "three"] * 3,
        "B": ["A", "B", "C"] * 4,
        "C": ["foo", "foo", "foo", "bar", "bar", "bar"] * 2,
        "D": np.random.randn(12),
        "E": np.random.randn(12)
    }
)

t=pd.pivot_table(df, values="D", index=["A","B"],columns=["C"])

## Time Zone
rng = pd.date_range("1/1/2012", periods=300, freq="s")
ts = pd.Series(np.random.randint(0, 500, len(rng)), index=rng)
t=ts.resample("1Min").sum()

## Categorical Data
df = pd.DataFrame(
    {"id": [1, 2, 3, 4, 5, 6], "raw_grade": ["a", "b", "b", "a", "a", "e"]}
)

df["grade"] = df["raw_grade"].astype("category")

new_categories = ["very good", "good", "very bad"]
df["grade"] = df["grade"].cat.rename_categories(new_categories)


print(df["grade"])