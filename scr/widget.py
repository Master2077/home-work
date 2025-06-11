from os import times

from masks import get_mask_account, get_mask_card_number

def mask_account_card(card_data: str) -> str:
   card_name_list = []
   account_name = ''
   card_number_list = []
   account_number = ''
   for i in card_data:
       if i.isalpha() or i == ' ':
           card_name_list += i
           account_name = ''.join(card_name_list)
   for i in card_data:
       if i.isdigit():
           card_number_list += i
           account_number = ''.join(card_number_list)
   return account_name + get_mask_card_number(account_number)




def get_date(time):
    day = time[8:10]
    month = time[5:7]
    year = time[0:4]
    return day + '.' + month + '.' + year




card_data_number = 'Visa Platinum 7000792289606361'
card_data_number_result = mask_account_card(card_data_number)
print(card_data_number_result)

card_data_account = 'Счет 73654108430135874305'
card_data_account_result = mask_account_card(card_data_account)
print(card_data_account_result)

time = "2024-03-11T02:26:18.671407"
time_result = get_date("2024-03-11T02:26:18.671407")
print(time_result)