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









card_data_number = 'Visa Platinum 7000792289606361'
card_data_number_result = mask_account_card(card_data_number)
print(card_data_number_result)

card_data_account = 'Счет 73654108430135874305'
card_data_account_result = mask_account_card(card_data_account)
print(card_data_account_result)