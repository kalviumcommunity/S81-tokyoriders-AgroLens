# Understanding the Machine Learning Workflow

This document explains how machine learning works as a decision pipeline, from raw data to monitored predictions. The focus is conceptual understanding.

## 1. The Complete Workflow

Machine learning is not one step. It is a sequence where each stage affects the next.

### Stage 1: Raw Data

Raw data is the original, unprocessed information collected from real systems. It can include logs, forms, transactions, sensor readings, text, images, or timestamps.

Raw data usually contains noise, missing values, duplicates, inconsistent units, and irrelevant fields. At this point, it is evidence, not yet a model-ready input.

### Stage 2: Feature Engineering

Features are measurable variables that the model can use to learn patterns. Feature engineering transforms raw data into useful signals.

Examples:
- Converting a transaction timestamp into hour of day
- Counting failed logins in the last 24 hours
- Encoding a category (for example, payment method)
- Normalizing monetary values

Important distinction:
- Raw data is what happened.
- Features are how we represent what happened for learning.

### Stage 3: Model Training

Training is the process where the model adjusts internal parameters to reduce error on historical examples.

Conceptually, the model sees many examples of:
- Feature vector $x$
- Known outcome $y$

It learns a mapping $f(x) \rightarrow y$ by repeatedly comparing predictions against true outcomes and updating parameters to improve fit.

In other words, the model does not memorize rows as facts to replay; it learns statistical relationships between feature patterns and outcomes.

### Stage 4: Prediction

After training, new unseen data is passed through the same feature pipeline. The trained model outputs:
- A class (for example, fraud or not fraud), or
- A score/probability (for example, fraud risk = 0.87), or
- A numeric estimate (for regression tasks)

Prediction quality depends on two conditions:
- New inputs must be transformed into features the same way as training data.
- The new data should resemble the data distribution the model learned from.

### Supporting Stage: Evaluation

Evaluation checks whether the model is useful before deployment.

This includes:
- Testing on data not used for training
- Using task-appropriate metrics (for example, precision/recall for fraud, MAE/RMSE for forecasting)
- Looking for error patterns across segments, not only one average score

Evaluation asks: "Is this model reliable enough for this decision context?"

### Supporting Stage: Monitoring

Monitoring continues after deployment.

It tracks:
- Data drift (input patterns changing)
- Concept drift (relationship between features and outcome changing)
- Performance decay over time
- Operational issues (latency, pipeline failures)

Monitoring asks: "Is the model still trustworthy in the real world today?"

## 2. Real-World Example: Credit Card Fraud Detection

### What is the raw data?

Raw data can include:
- Transaction amount
- Merchant ID/category
- Timestamp
- Cardholder location
- Device information
- Historical transaction logs
- Chargeback labels collected later

### What are the features?

Engineered features might include:
- Number of transactions in last 10 minutes
- Distance from previous transaction location
- Average transaction amount for this user in past 30 days
- Whether amount is unusually high relative to user baseline
- Risk score of merchant category

These features encode behavior and context that make fraud patterns learnable.

### What does the model learn?

The model learns probabilistic patterns that separate normal behavior from suspicious behavior, such as:
- Sudden high-value purchases after a long idle period
- Fast cross-region transactions impossible for a single cardholder
- A sequence of small tests followed by a large charge

It learns these as weighted relationships among features, not as human-written rules.

### What does the prediction represent?

The prediction is typically a fraud risk score or class label for each new transaction.

Example interpretation:
- Score = 0.02: likely legitimate
- Score = 0.91: high fraud risk, trigger review or block

So prediction is an estimate of risk for action, not a guaranteed truth.

## 3. Failure Scenario: Data Leakage During Training

### What can go wrong?

A leaked feature accidentally includes future information unavailable at prediction time.

Example in fraud detection:
- A training feature indirectly uses chargeback status that is known days after the transaction.

The model appears excellent in offline evaluation because it is learning from hidden future clues.

### Why is this dangerous?

- Offline metrics look unrealistically high.
- Stakeholders trust the model and deploy it.
- Real-world performance drops because leaked information does not exist at inference time.
- Operational decisions become unreliable (missed fraud or false blocks).

### Core lesson

Good performance numbers are meaningful only when feature generation reflects real-time availability. If time logic is wrong, the entire workflow is compromised.

## 4. Quick Mental Model

Use this sequence to reason about any ML system:

1. What happened? (raw data)
2. How is it represented? (features)
3. What relationship is learned? (training)
4. What action signal is produced? (prediction)
5. How do we know it works and keeps working? (evaluation + monitoring)

If any one stage is weak, downstream outputs become unreliable.