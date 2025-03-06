def luhn_check(str_number):
    digits = list(map(int, str_number))  
    even_sum = sum(digits[-1::-2])  
    # debug  print(f"Even sequence {digits[-1::-2][::-1]} ")
    # debug print(f"Sum even {even_sum} ")
    odds_sum=0
    for d in digits[-2::-2]:
        if (2*d)>9:
            odds_sum+=(2*d)-9
        else:
            odds_sum+=(2*d) 
    # debug print(f"Odds Sequence {digits[-2::-2][::-1]} ")
    # debug print(f"Odds sum {odds_sum} ")
    return  ((odds_sum + even_sum)%10 ==0)

# check is congruent to mod 10
test_number = input("Credit Card Number:-").replace(' ','') 
# debug print(f"Credit card Number {test_number}  ")
# debug print(f"The credit card check digit is {test_number[-1]}")
print(f"Luhn Check Passes? {luhn_check(test_number)}")


