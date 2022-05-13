Triggers:
1)create or replace trigger update_cust_purchases after insert 
    on connect_customers_purchase for each row
    declare
    v_bank_id Number;
    v_discount_id Varchar2(15);
    v_last Number;
    v_new_total_purchases Number;
    begin 
    Select bank_card_id into v_bank_id from connect_customers where id = :new.cust_id;
    -- update the total purchases of the customer
    update connect_customers set total_purchases = total_purchases + :new.total_sum where id = :new.cust_id;
    -- update the discount of the customer 
    Select total_purchases into v_new_total_purchases from connect_customers where id = :new.cust_id;
    Select id into v_last from connect_discounts where starter_sum> v_new_total_purchases and rownum=1;
    Select discount_id into v_discount_id from connect_discounts where id = v_last-1;
    update connect_customers set discount_id = v_discount_id where id = :new.cust_id;
    -- update the consultant's sales sum
    update connect_consultants set sales_sum = sales_sum + :new.total_sum where id = :new.consultant_id;
    -- update the bank's total transactions
    update connect_bank_card set total_transactions = total_transactions + :new.total_sum where id = v_bank_id;
    end;
2)create or replace trigger update_articles_size 
      after insert on connect_purchases for each row
      declare 
      v_type_id Number;
      begin
      case :new.sizes
      when 'XS' then update connect_articles set XS = XS - :new.amount where article = :new.article_id;
      when 'S' then update connect_articles set S = S - :new.amount where article = :new.article_id;
      when 'M' then update connect_articles set M = M - :new.amount where article = :new.article_id;
      when 'L' then update connect_articles set L = L - :new.amount where article = :new.article_id;
      end case;
      select type_id into v_type_id from connect_articles where article = :new.article_id;
      update connect_product_types set amount = amount - :new.amount where id = v_type_id;
      end;
3)create or replace trigger insert_articles 
  after insert on connect_articles for each row 
  begin
  update connect_product_types set amount = amount + (:new.XS + :new.S + :new.M + :new.L) where id = :new.type_id;
  end;

Functions:
1)create or replace procedure edit_consultants(p_id in Number,p_name in varchar2,p_surname in varchar2 ,p_sales_sum in Number,p_image in varchar2,p_gender in varchar2) is

  begin
  update connect_consultants set name = p_name, surname = p_surname, sales_sum = p_sales_sum, image = p_image, gender = p_gender
  where id = p_id;
  end;
2)create or replace procedure delete_consultants(p_id in Number) is
  
  begin
  delete from connect_consultants where id = p_id;
  end;
3)create or replace function search_consultants(p_name in varchar2, p_id in number) return connect_consultants%ROWTYPE is 
  v_result connect_consultants%ROWTYPE;
  cursor v_consultant is select * from connect_consultants where name = p_name or id = p_id;
  begin
  for consultant in v_consultant loop
  return consultant;
  end loop;
  end;
4)create or replace procedure edit_discount(p_id in Varchar2, p_percent in Number, p_starter_sum in Number) is

  begin
  update connect_discounts set percent = p_percent, starter_sum = p_starter_sum
  where id = p_id;
  end;
5)