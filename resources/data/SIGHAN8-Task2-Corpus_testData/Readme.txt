SIGHAN 8 -Task 2
Task 2: Topic-Based Chinese Message Polarity Classification

Description :Topic-Based Chinese Message Polarity Classification: 
Given a message from Chinese Weibo Platform (Such as Sina, Tencent，NetEase etc. ) and a topic, 
classify whether the message is of positive, negative, or neutral sentiment towards the given 
topic. For messages conveying both a positive and negative sentiment towards the topic, whichever 
is the stronger sentiment should be chosen.

Each participant is required to submit two kinds of results based on: 
(1) restricted resource for fair comparison, e.g. same sentiment lexicon, corpus, etc. that will 
be announced together with the test data; and (2) unrestricted resource. We believe that a freely 
available, annotated corpus that can be used as a common testbed is needed in order to promote 
research that will lead to a better understanding of how sentiment is conveyed in tweets and texts. 

Output format: We expect the following format for the output file:

runId <TAB> topicID <TAB> evalID<TAB> mesID <TAB>Polarity  

Where

runID is the ID of each participant run,  

topicID is the ID of each topic,

evalID can be “0 for restricted test ” or“1 for unrestricted test”，

mesID is message ID,

and Polarity can be predicted sentimentpolarity of topic ("1 for positive", "-1 for negative" or
"0 for neutral").

For example, topic “iphone6”  ( TopicID T1),

<M15113801> 苹果公司已经发布了新产品iphone6 </M15113801>

<M15113803> iphone6运行速度快，还是不错的</M15113803>.

<M15113805> 但是，iphone6好像太薄了，容易折断，另外摄像头怎么是凸出的啊</M15113805>

Output file:

NA <TAB> T1 <TAB>1 <TAB> M15113801 <TAB> 0

NA <TAB> T1 <TAB>1 <TAB> M15113803 <TAB> 1       

NA <TAB> T1 <TAB>1 <TAB> M15113805 <TAB> -1

-----------------------------
The file TopicID.txt format:

topicID <TAB> topic