# Spam-Filter
 Using Naive Bayes theorem to create a spam filter trained on data classified as spam and not spam.
 We use the following formulas:
 The formula used by the software to determine that, is derived from Bayes' theorem

Pr(S|W)=Pr(W|S).P(S)/{Pr(W|S).Pr(S)+Pr(W|H).Pr(H)}
where:

Pr(S|W) is the probability that a message is a spam;

Pr(S) is the overall probability that any given message is spam;

Pr(W|S) is the probability that the word appears in spam messages;

Pr(H) is the overall probability that any given message is not spam (is "ham");

Pr(W|H) is the probability that the word appears in ham messages.
