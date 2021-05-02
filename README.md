# My-GRE-Dict
**A simple web app to create and maintain your own GRE dictionary.**

**Features**

-You can initialize the database with 1000 words from magoosh.<br>
-You can always add new words.<br>
-You can search any existing word.<br>
These are the basic needs.<br>

Now, what makes this thing useful is the order that the words come up. You can simply set a weight for the current word and based on that the system will decide when to show it next. The lower the weight, the later you'll see it next.
So, if you don't wanna see any word anytime soon, just set the weight to 0 or very low. The system will take care of the rest. Or you can set the order as alphabatical.

If you really wanna know the calculation behind, the source code is there...you'll find it in 'views.py'.

**System Requirements**

You just need to have Django environment set up. I had django 2.0.7 with python 3.6.13 installed in my pc. Any version compatible should be okay. If you lack any package or something, just install it right away.
Here's a link if you need help to set up the environment - 
https://www.codingforentrepreneurs.com/getting-started

If you have the following UIs, you're good.


![0](https://user-images.githubusercontent.com/29086609/116823846-aec60300-aba8-11eb-8697-8796c2961b03.png)
![1](https://user-images.githubusercontent.com/29086609/116823833-9ce46000-aba8-11eb-8d2c-a0634757c307.png)
![2](https://user-images.githubusercontent.com/29086609/116823831-9bb33300-aba8-11eb-9000-b49745a4f1eb.png)
![3](https://user-images.githubusercontent.com/29086609/116823830-9b1a9c80-aba8-11eb-93d2-9bfe9078f347.png)
![4](https://user-images.githubusercontent.com/29086609/116823826-981fac00-aba8-11eb-843f-1d9882581cb4.png)
