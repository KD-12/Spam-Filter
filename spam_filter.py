import argparse
import re
import csv

def training_phase(train_list):
    """
    Based on the input training data set this function calculate the individual probabilities
    of the words commonly occuring in both spam and ham e-mails
    The approach used is:
    1. Split the words of e-mails of training data set into spam and ham category
    2. Calculate the net probability of spam and ham emails in training dataset
    3. Calculate the Probability of a word given it appears in Spam/Ham email
    """
    ham_count=0
    msg_count = 0
    p_ham = 0.0
    p_spam = 0.0

    ham_split_list = []
    spam_split_list = []
    all_split_list = []
    ham_word_d = {}
    spam_word_d = {}
    all_word_d = {}

    for i in train_list:
        msg_count += 1

        match = re.search('ham', i)
        if match:
            ham_count += 1
            ham_split_list = i.split()
            for j in xrange(2, len(ham_split_list)-1, 2):
                if (ham_split_list[j] in ham_word_d):
                    ham_word_d[ham_split_list[j]] = ham_word_d[ham_split_list[j]] + float(ham_split_list[j+1])
                else:
                    ham_word_d[ham_split_list[j]] = float(ham_split_list[j+1])

                if (ham_split_list[j] in all_word_d):
                    all_word_d[ham_split_list[j]] = all_word_d[ham_split_list[j]] + float(ham_split_list[j+1])
                else:
                    all_word_d[ham_split_list[j]] = float(ham_split_list[j+1])
        else :
            spam_split_list = i.split()
            for j in xrange(2, len(spam_split_list)-1, 2):
                if (spam_split_list[j] in spam_word_d):
                    spam_word_d[spam_split_list[j]] = spam_word_d[spam_split_list[j]] + float(spam_split_list[j+1])
                else:
                    spam_word_d[spam_split_list[j]] = float(spam_split_list[j+1])

                if (spam_split_list[j] in all_word_d):
                    all_word_d[spam_split_list[j]] = all_word_d[spam_split_list[j]] + float(spam_split_list[j+1])
                else:
                    all_word_d[spam_split_list[j]] = float(spam_split_list[j+1])

    #Calculate  probability of ham and spam messages in training data dataset
    p_ham = (ham_count*1.0)/(msg_count*1.0)
    p_spam = 1.0 - p_ham

    #To calculate the p(word|spam)
    prob_word_spam = {}
    for key in spam_word_d:
            prob_word_spam[key] = (1.0 * spam_word_d[key])/(1.0 * all_word_d[key])

    #To calculate the p(word|ham)
    prob_word_ham = {}
    for key in ham_word_d:
            prob_word_ham[key] = (1.0 * ham_word_d[key])/(1.0 * all_word_d[key])

    return p_spam, p_ham, prob_word_spam, prob_word_ham

def classification(p_spam, p_ham, prob_word_spam, prob_word_ham, message):
    """
    This function clasifies the input message by calculating the probability that
    the email(message) is Spam
    """
    prob = 0.0
    checklist = []
    checklist = message.split()
    checklist_d = {}

    for i in xrange(2, len(checklist), 2):
        #Default smoothing value used in case the new word is not categorized as spam or ham before
        pr_w_s = 0.001
        pr_w_h = 0.001
        #We initialize both p_spam and p_ham equal probabilities as there is no a priori reason for an e-mail to be spam or ham
        p_spam = 0.5
        p_ham = 0.5
        if checklist[i] in prob_word_spam:
            pr_w_s = prob_word_spam[checklist[i]]
        if checklist[i] in prob_word_ham:
            pr_w_h = prob_word_ham[checklist[i]]
        #Use of Bayes Theorem, to compute that the message containing given word is a spam
        checklist_d[checklist[i]] = (((pr_w_s)*(p_spam)))/((((pr_w_s)*(p_spam)) + ((pr_w_h)*(p_ham))))

    p_value = 1.0
    for i in checklist_d:
        p_value = (1.0 * p_value)*(1.0 * checklist_d[i])

    p_value_not = 1.0
    for i in checklist_d:
        p_value_not = (1.0 * p_value_not)*(1.0 - checklist_d[i])

    #Combining individual probabilities to get the net value
    prob = (1.0 * p_value)/((1.0 * p_value) + (1.0 * p_value_not))

    return prob

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f1', help='training file', required=True)
    parser.add_argument('-f2', help='test file', required=True)
    parser.add_argument('-o', help='output labels for the test dataset', required=True)

    args = vars(parser.parse_args())
    Xtrain_name = args['f1']
    Xtest_name = args['f2']

    XOut_name = args['o']
    print "Train file : ",  Xtrain_name
    print "Test file : ",  Xtest_name
    f1 = open(Xtrain_name, 'r')
    with open(Xtrain_name) as f:
        train_list = f.readlines()

    trained_prob = 0.0
    prob_word_spam = {}
    prob_word_ham = {}
    p_spam = 0.0
    p_ham = 0.0
    p_spam, p_ham, prob_word_spam, prob_word_ham = training_phase(train_list)

    with open(Xtest_name) as f:
        test_list = f.readlines()

    with open(XOut_name, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        spamwriter.writerow(['<ID>    '] + ['<Spam/Ham>'])

        temp = []
        actual_cnt = 0
        calculated_cnt = 0
        for i in test_list:
            temp = i.split()

            actual_cnt += 1
            trained_prob = classification(p_spam, p_ham, prob_word_spam, prob_word_ham, i)
            if (trained_prob > 0.5):
                if (temp[1] == 'spam'):
                    calculated_cnt += 1
                spamwriter.writerow([temp[0]] + ['Spam'])
            else:
                if (temp[1] == 'ham'):
                    calculated_cnt += 1
                spamwriter.writerow([temp[0]] + ['Ham'])

    print "actual email count in test data set : ", actual_cnt
    print "correctly classifed email count : ", calculated_cnt
    accuracy = 0.0
    accuracy = (1.0 * calculated_cnt)/(1.0 * actual_cnt)
    print "Accuracy : ", accuracy
