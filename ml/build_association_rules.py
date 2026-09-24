import pandas as pd
import joblib
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules

print("Loading Skill Transactions...")
with open('data/skill_transactions.csv', 'r') as f:
    transactions = [line.strip().split(',') for line in f.readlines()]

te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_)

print("Running FP-Growth...")
# Find frequent itemsets
frequent_itemsets = fpgrowth(df, min_support=0.05, use_colnames=True)

print("Building Association Rules...")
# Generate rules
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.3)

print(f"Generated {len(rules)} rules.")
print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))

# Save rules for recommendations
joblib.dump(rules, 'models/skill_rules.pkl')
print("\nSaved rules to models/skill_rules.pkl")
