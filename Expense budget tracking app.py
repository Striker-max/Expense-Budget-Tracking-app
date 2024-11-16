### --- Compulsory Task: Capstone Project - Tracker App --- ###
#=====Importing Required Libraries=====
import sqlite3
from tabulate import tabulate

#=====Function Section=====
# Check that inputs are integers
def integer_check(choice):
    while True:  
        try: 
            return int(choice)
        except ValueError:
            print("Invalid entry. Please enter an integer.")
            sec_choice = input()
            return integer_check(sec_choice)
        

# Ensures same ID isn't used twice and updates tables
def unique_id(new_entry):
    while True:
        try:
            cursor.execute('''INSERT INTO transactions(id, type, category, 
                           amount) VALUES(?, ?, ?, ?)''', (new_entry))
            db.commit()
            break
        except sqlite3.IntegrityError:
            print("Invalid entry. Please enter a different ID.")
            new_id = input()
            updated_entry = list(new_entry)
            updated_entry[0] = int(new_id)
            new_entry = tuple(updated_entry)
            return unique_id(new_entry)


# Sets up transactions table from finances database
def complete_transaction_table():
    cursor.execute('''SELECT * FROM transactions''')
    view_transactions = cursor.fetchall()
    return view_transactions


# Checks that correct inputs are given for update choice (Y/N)
def choice_check(choice):
    current_choice = choice.upper()
    if current_choice == 'Y' or current_choice == 'N':
        return current_choice
    else:
        new_choice = input("Invalid entry. Please enter Y or N.\n")
        return choice_check(new_choice)


# Edit expense amount
def amt_change(id_choice):
    full_table = complete_transaction_table()
    valid_transaction = 0
    for transaction in full_table:
        if transaction[0] == id_choice:
            new_amount = input("Please enter new amount: ")
            checked_amount = integer_check(new_amount)
            valid_transaction = 1
    if valid_transaction == 0:      
          print("Provided id does not exist in transactions table.")
    else:
        cursor.execute('''UPDATE transactions SET amount = ? 
                        WHERE id = ?''', (checked_amount, id_choice))
        db.commit()
        print("Transaction amount updated in database.")


# Display income or expense transactions table from database
def transaction_table(trans_type):
    col_names = ['ID', 'Type', 'Category', 'Amount(R)']
    cursor.execute('''SELECT * FROM transactions WHERE type = ?''', 
                   (trans_type,))
    view_transactions = cursor.fetchall()
    print(tabulate(view_transactions, col_names, tablefmt = 'grid'))
    return view_transactions


# Extract categories from transaction table
def cat_list(trans_type):
    cursor.execute('''SELECT category FROM transactions WHERE type = ?''', 
                   (trans_type,))
    categories = cursor.fetchall()
    categories_list = [category[0] for category in categories]
    no_duplicates = list(set(categories_list))
    return no_duplicates 


# Check that valid category is given
def cat_check(cat_list, choice):
    if choice in cat_list:
        return choice
    else:
        new_choice = input(
'''Invalid entry. Please input a category from the list. ''')
        return cat_check(cat_list, new_choice)


# Display income or expense transactions table from database by category
def cat_table(trans_type, cat_choice):
    col_names = ['ID', 'Type', 'Category', 'Amount(R)']
    cursor.execute('''SELECT * FROM transactions WHERE type = ? and 
                   category = ?''', (trans_type, cat_choice,))
    view_transactions = cursor.fetchall()
    print(tabulate(view_transactions, col_names, tablefmt = 'grid') + "\n")
    return view_transactions


# Delete records from the transactions table by category
def delete_category(cat_choice):
    full_table = complete_transaction_table()
    del_count = 0
    for transaction in full_table:
        if transaction[2] == cat_choice:
            cursor.execute('''DELETE FROM transactions WHERE category = ?''', 
                           (cat_choice,))
            db.commit()
            del_count += 1
    if del_count >= 1:
        print("Transactions with corresponding categories deleted.\n")
    else:
        print("No such transactions in database.\n")


# Lists all budgets in the budgets table
def budget_list():
    cursor.execute('''SELECT category FROM budgets''')
    cats = cursor.fetchall()
    cats_list = [categories[0] for categories in cats]
    return cats_list


# Extract chosen budget from budgets table
def budget_amount(cat):
    cursor.execute('''SELECT amount FROM budgets WHERE category = ?''', (cat,))
    amount = cursor.fetchone()
    return amount[0]


# Add the amounts together for a specified category
def amount_sum(cat_type):
    cursor.execute('''SELECT amount FROM transactions WHERE category = ?''', 
                   (cat_type,))
    amounts = cursor.fetchall()
    amounts_list = [amount[0] for amount in amounts]
    total_amount = sum(amounts_list)
    return total_amount 


#=====Database Section=====
# Create database named 'finances' and table named 'transactions'
db = sqlite3.connect('finances_db.db')
cursor = db.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
               (id INTEGER PRIMARY KEY, type TEXT, category TEXT, 
               amount INTEGER)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS budgets
               (category TEXT PRIMARY KEY, amount INTEGER)''')
db.commit()

#=====Menu Section=====
#budget_dictionary = {}
while True:
    menu_entry = input('''Please select one of the following options:
1. Add expense
2. View expenses
3. View expenses by category
4. Add income
5. View income
6. View income by category
7. Set budget for a category
8. View budget for a category
9. Set financial goals
10. View progress towards financial goals
11. Quit                            
''')
    menu_choice = integer_check(menu_entry)

# Add expenses to the transactions table          
    if menu_choice == 1:
        new_id = input("Please enter new expense ID: ")
        checked_id = integer_check(new_id)
        new_type = "Expense"
        new_category = input("Please enter new expense category: ")
        new_amount = input("Please enter amount for new expense: ")
        checked_amount = integer_check(new_amount)
        new_expense = (checked_id, new_type, new_category, checked_amount)
        unique_id(new_expense)
        print("New expense added to database.\n")
        continue

# View expenses in the transactions table     
    elif menu_choice == 2:
        trans_type = "Expense"
        transaction_table(trans_type)
        change_amount = input("Would you like to update an amount? (Y/N): ")
        edit_amount = choice_check(change_amount)
        if edit_amount == 'Y':
            id_input = input(
'''Please provide id of transaction amount that needs to be updated. ''')
            id_choice = integer_check(id_input)
            amt_change(id_choice)
        elif edit_amount == 'N':
            print("No changes made.")
        del_cat = input(
'''Would you like to delete one of the transaction categories? (Y/N): ''')
        del_choice = choice_check(del_cat)
        if del_choice == 'Y':
            check_categories = cat_list(trans_type)
            print(', '.join(check_categories))
            del_category = input(
'''Which of the abovementioned categories should be deleted? ''')
            check_del_category = cat_check(check_categories, del_category)
            delete_category(check_del_category)
        elif del_choice == 'N':
            print("No categories deleted from database.\n")
        continue

# View expenses in the transactions table by category 
    elif menu_choice == 3:
        trans_type = "Expense"
        options = cat_list(trans_type)
        print(', '.join(options))
        cat_choice = input(
'''Please select one of the abovementioned categories: ''')
        checked_cat = cat_check(options, cat_choice)
        cat_table(trans_type, checked_cat)
        continue

# Add new income to the transactions table 
    elif menu_choice == 4:  
        new_income_id = input("Please enter new income ID: ")
        checked_income_id = integer_check(new_income_id)
        transaction_type = "Income"
        new_income_category = input("Please enter new income category: ")
        new_income_amount = input("Please enter amount for new income: ")
        checked_income_amount = integer_check(new_income_amount)
        new_income = (checked_income_id, transaction_type, new_income_category, 
                      checked_income_amount)
        unique_id(new_income)
        print("New income added to database.\n")
        continue

# View income in the transactions table
    elif menu_choice == 5:  
        transaction_type = "Income"
        transaction_table(transaction_type)
        delete_cat = input(
'''Would you like to delete one of the transaction categories? (Y/N): ''')
        delete_choice = choice_check(delete_cat)
        if delete_choice == 'Y':
            check_in_categories = cat_list(transaction_type)
            print(', '.join(check_in_categories))
            del_in_category = input(
'''Which of the abovementioned categories should be deleted? ''')
            check_in_del_category = cat_check(check_in_categories, 
                                              del_in_category)
            delete_category(check_in_del_category)
        elif delete_choice == 'N':
            print("No categories deleted from database.\n")
        continue

# View income in the transactions table by category
    elif menu_choice == 6:  
        transaction_type = "Income"
        choices = cat_list(transaction_type)
        print(', '.join(choices))
        category_choice = input(
'''Please select one of the abovementioned categories: ''')
        checked_category = cat_check(choices, category_choice)
        cat_table(transaction_type, checked_category)
        continue

# Set up a budget for a selected category
    elif menu_choice == 7:  
        trans_type = "Expense"
        category_list = cat_list(trans_type)
        print(', '.join(category_list))
        exp_budget_choice = input("For which category? ")
        checked_bud_cat = cat_check(category_list, exp_budget_choice)
        max_exp = input(
f'Please enter your budget for the {checked_bud_cat} category: ')
        cursor.execute('''INSERT INTO budgets(category, amount) 
                       VALUES(?, ?)''', (checked_bud_cat, max_exp))
        db.commit()
        print("Budget added\n")
        continue

# View budget for a selected category
    elif menu_choice == 8:  
        avail_budgets = budget_list()
        print(f'Budgets: {', '.join(avail_budgets)}')
        budget_exp_choice = input("Which budget would you like to view? ")
        budget_choice = cat_check(avail_budgets, budget_exp_choice)
        budgeted_amount = budget_amount(budget_choice)
        print(f'{budget_choice} budget = R{budgeted_amount}')
        cur_expense = amount_sum(budget_choice)
        print(f"Current expenditure = R{cur_expense}")
        exp_diff = budgeted_amount - cur_expense
        print(f"Difference between budget and expenditure = R{exp_diff}")
        if exp_diff >= 0:
            print("Status: Still within budget.\n")
        else:
            print("Status: Over-budget!\n")
        continue   

# Set up financial goals
    elif menu_choice == 9:  
        fin_goal = input(
'''How much money would you like to have remaining after deductions? ''')
        print("Thank you. Financial goal saved.\n")
        continue 

# View progress to financial goals
    elif menu_choice == 10:  
        try:
            fin_goal
        except NameError:
            fin_goal = input(
'''How much money would you like to have remaining after deductions? ''')
        debits = "Income"
        credits = "Expense"
        i = 0
        j = 0
        headers = ["Financial category", "Amount(R)"]
        debit_list = cat_list(debits)
        debit_totals = [0] * len(debit_list)
        for debit_total in debit_list:
            debit_totals[i] = amount_sum(debit_list[i])
            i+=1
        credit_list = cat_list(credits)
        credit_totals = [0] * len(credit_list)
        for credit_total in credit_list:
            credit_totals[j] = amount_sum(credit_list[j])
            j += 1
        fin_prog = sum(debit_totals) - sum(credit_totals)
        rem_prog = int(fin_goal) - fin_prog
        if rem_prog <= 0:
            rem_prog = 0
        fin_cats = [debits, credits, "Financial goal", "Net income", 
                    "Remaining progress required"]
        fin_amts = [sum(debit_totals), sum(credit_totals), fin_goal, fin_prog, 
                    rem_prog]
        total_entries = list(zip(fin_cats, fin_amts))
        print(f"{tabulate(total_entries, headers, tablefmt = 'grid')}")
        if rem_prog <= 0:
            print("Financial goal achieved!\n")
        continue 

# Exit database 
    elif menu_choice == 11:
        print("Goodbye!")
        break 

# Restart loop if incorrect input given for menu_choice
    else:
        print("Invalid input. Please try again.\n")

# Close database
db.close() 

