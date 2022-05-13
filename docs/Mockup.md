                                       IMAGE 1
For search by subtype_id: SELECT XS,S,M,L from Subtypes_of_ProductTypes where subtype_id=input;
 
for every user of the site,web page creates a new table with the additional column named "is_in_basket",
to save info whether the user liked the product
CREATE TABLE Subtypes_for_customers AS SELECT * from Subtypes_of_ProductTypes;
ALTER table Subtypes_for_customers ADD COLUMN is_in_basket varchar(5); 

for liked products(избранные):update Subtypes_for_customers set is_in_basket = "Yes" where subtype_id = input;

                                    IMAGE 2
1)For every purchase in the site , program creates a random purchase_id.

2)When customer enters the size and amount of the specified product:
First step:Insert into Purchases values(purchase_id(randomly generated),subtype_id(input), type_id(input), size(input), amount(input));
Second step: Create trigger Trigger_1 after insert on Purchases
  BEGIN
     update Subtypes_Of_ProductTypes set 
  case when size = 'S' then S = S-amount,
  when size = 'XS' then XS = XS - amount,
  when size = 'L' then L = L - amount,
  when size = 'M' then M = M - amount END
  where subtype_id = subtype_id(input);
     update Product_Types set
  amount = amount-amount(input)
  where type_id = type_id(input);
  END

3)To calculate the total sum:(now the total sum is saved in the computer's memory)
Select sum(amount*price) as total_sum from Purchases 
join Subtypes_Of_ProductTypes on Purchases.subtype_id = Subtypes_Of_ProductTypes.subtype_id
where purchase_id = purchase_id(randomly generated);

4)When customer enters a name, surname, bankcard and cvv , the program checks whether the customer is in the table Customers or not:
   Select id from Customers where first_name = name(input) AND last_name = surname(input) AND bank_card_no = bankcard(input) AND CVV = CVV(input);
   After clicking the button "Check out":

1-case:if the id is null, create a new row (id is autoincremented)for the current customer to the table Customers:
   Insert into Customers Values(name(input), surname(input), purchase_id(randomly generated),gender(determined by the program),bank_card_no(input, expiration_date(input), CVV(input), total_sum(saved in the memory), null(because the customer is new));
Then insert it into Customers_Purchase table:
   Create trigger Trigger_2 after insert on Customers
   BEGIN
   Insert into Customers_Purchase VALUES(new.id, date(today's date), new.purchase_id, bank_card_id(determined by the program), new.total_purchases, null(purchase is made online));
   END

2-case:If the id of the customer is already in the table Customers, retrieve its discount percent(if exists):
   Select Discounts.percent from Customers join Discounts on Customers.discount_id =Discounts.id where Customers.id = (Select id from Customers where first_name = name(input) AND last_name = surname(input) AND bank_card_no = bankcard(input) AND CVV = CVV(input));
   If the percent is not null(it means the customer has a discount):
The customer is asked, if she wants to use the discount and shows the updated total_sum(calculated by program ((1-percent/100)*total_sum)). If the customer checks the box, total sum is inserted with updated valuecalculated by the program to the table Customers_Purchase, else (discount is null or the customer doesn't want to use the discount) the total_sum remains with previous value:
   Insert into Customers_Purchase VALUES(id, date(today's date),purchase_id(randomly generated), bank_card_id(determined by the program), total_sum, null);

Whenever the case is appeared, bank_card table's total_transaction is updated after inserting information to Customers_Purchase:
   Create trigger Trigger_3 after insert into Customers_Purchase
   BEGIN
   Update Bank_card set total_transactions = total_transactions+total_sum
   where id = new.bank_card_id;
   END
                                             
                                              IMAGE 3
1)After all informations are entered, randomly generated purchase_id is created by the program, then all entered subtypes with size and amount are added to Purchases table:
   Insert into Purchases VALUES(purchase_id(randomly generated), subtype_id, size, amount);
   Create trigger Trigger_6 after insert into Purchases 
   BEGIN
   Update Subtypes_Of_ProductTypes set 
   case when size = 'XS' then XS = XS-amount(input),
        when size = 'S' then S = S-amount(input),
        when size = 'L' then L = L-amount(input),
        when size = 'M' then M = M -amount(input)
   where subtype_id = subtype_id(input);

   Update Product-Types set amount = amount- amount(input) 
   where type_id = (Select t_id from Subtypes_Of_ProductTypes where subtype_id = subtype_id(input));
   END

2)Calculate the total sum of the purchase:
   Select sum(amount*price) from Purchases join Subtypes_Of_ProductTypes s on Purchases.subtype_id = s.subtype_id where purchase_id = purchase_id(input);

3)Checks whether the customer is in the table Customer, if it is not, create a new customer row :
   Select id from Customers where name = first name(input) AND surname = Last name(input) and bank_card_no = bankcard_no(input) and CVV = CVV(input);
1-case: if id is null, new row is created for the customer and inserted into Customers:
   Insert into Customers VALUES(id(is autoincremented), first name(input), Last name(input), gender(input), bank_card_no(input), expiration_date(input), CVV(input), (Select sum(amount*price) from Purchases join Subtypes_Of_ProductTypes s on Purchases.subtype_id = s.subtype_id where purchase_id = purchase_id(input)), null);

   Create trigger Trigger_7 after insert on Customers
   BEGIN
   Insert into Customers_Purchases VALUES(new.id, today's date, purchase_id(randomly generated), bank_card_id(input), new.total_purchases, consultant_id(input));

2-case: if id is not null:
   Update Customers set total_purchases = total_purchases + (Select sum(amount*price) from Purchases join Subtypes_Of_ProductTypes s on Purchases.subtype_id = s.subtype_id where purchase_id = purchase_id(input)) where id = (Select id from Customers where name = first name(input) AND surname = Last name(input) and bank_card_no = bankcard_no(input) and CVV = CVV(input)) *(1 - (Select percent from Customers join Discounts on Customers.discount_id = Discounts.id where id = (Select id from Customers where name = first name(input) AND surname = Last name(input) and bank_card_no = bankcard_no(input) and CVV = CVV(input)))/100);

   Create trigger Trigger_8 after update on Customers 
   BEGIN
   Insert into Customers_Purchases Values((Select id from Customers where name = first name(input) AND surname = Last name(input) and bank_card_no = bankcard_no(input) and CVV = CVV(input)), today's date, purchase_id(randomly generated), bank_card_id(input), new.total_purchases- old.total_purchases, consultant_id(input));
   END

   Create trigger Trigger_9 after insert on Customers_Purchases
   BEGIN
   Update Consultants set sales_sum = sales_sum + new.total_sum 
   where id = consultant_id(input);
   END

   Create trigger Trigger_10 after insert on Customers_Purchases
   BEGIN
   Update Bank_card set total_transactions = total_transactions + new.total_sum
   where id = new.bank_card_id;
   END
                                           IMAGE 4 (part 1)
1)When the subtype_id is entered and size is selected this query is executed to show type_id, amount of the specified size and price :
    select p.type_id, (
    case 
    when input.size = 'XS' then s.XS,
    when input.size  = 'S' then s.S,
    when input.size  = 'L' then s.L,
    when input.size  = 'M' then s.M
    else end
    ) as size_amount, Subtypes_of_ProductTypes.price 
    from Subtypes_of_ProductTypes s
    join Product_Types p on s.t_id = p.type_id
    where s.subtype_id == input.subtype_id;
                                            
                                            IMAGE 4 (part 2)
1)After inputs are entered, the return money is calculated and shown in the screen:
    Select price*amount(input) as return_money from Subtypes_Of_ProductTypes where subtype_id = subtype_id(input);
After return money is calculated and "Confirm button" is clicked, all informations are inserted into the table Return_list:
    INSERT INTO Return_list Values(purchase_id(input),subtype_id(input),amount(input), (Select price*amount(input) as return_money from Subtypes_Of_ProductTypes where subtype_id = subtype_id(input)));

    Create trigger Trigger_3 after insert on Return_list
    BEGIN
    Update Purchases set amount = amount-amount(input)
    where purchase_id = purchase_id(input) and subtype_id = subtype_id(input);

    Update Subtypes_Of_ProductTypes set 
    case when (Select size from Purchases where purchase_id = purchase_id(input) and subtype_id = subtype_id(input)) = 'XS' 
    then XS = XS+amount(input),
        when (Select size from Purchases where purchase_id = purchase_id(input) and subtype_id = subtype_id(input)) = 'S' 
    then S = S+amount(input),
        when (Select size from Purchases where purchase_id = purchase_id(input) and subtype_id = subtype_id(input)) = 'M' 
    then M = M +amount(input),
        when (Select size from Purchases where purchase_id = purchase_id(input) and subtype_id = subtype_id(input)) = 'L' 
    then L = L +amount(input) END
    where subtype_id = subtype_id(input);

    Update Product_Types set
    amount = amount + amount(input) where type_id = (select t_id from Subtypes_Of_ProductTypes where subtype_id = subtype_id(input));

    Delete * from Purchases where amount = 0;

    Update Bank_card set total_transactions = total_transactions - (Select price*amount(input) from Subtypes_Of_ProductTypes where subtype_id = subtype_id(input);) where id = (select bank_card_id from Customers_Purchase where purchase_id = purchase_id(input));

    Update Customers_Purchase set total_sum = total_sum - (Select price*amount(input) from Subtypes_Of_ProductTypes where subtype_id = subtype_id(input);) where id = (select bank_card_id from Customers_Purchase where purchase_id = purchase_id(input)) where 
    purchase_id = purchase_id(input);

    Update Customers set total_purchases = total_purchases - (Select price*amount(input) from Subtypes_Of_ProductTypes where subtype_id = subtype_id(input);) where id = (select bank_card_id from Customers_Purchase where purchase_id = purchase_id(input)) 
    where id = (Select cust_id from Customers_Purchase where purchase_id = purchase_id(input));
    END
                                            



  
