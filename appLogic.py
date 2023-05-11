from logic import notify 
from logic import sqlQueries 

# have to confirm joining mail list or confirm 
# def confirm(email, type):
#     if(type == "joinForm"):
#         sendJoinEmail(email)
#     if(type == "update"):
#         sendUpdateEmail(email)
        
def join(email, pref):
    # check if they are already in database, if not do nothing? Or get them to restart the process of joining
    inDB = sqlQueries.isUser(email)

    # send email to given email prompting them to join the confirm link to join list. 
    if(not inDB):
        sqlQueries.createUser(email, pref)

def update(email, pref):
    # check if they are already in database, if not do nothing? Or get them to restart the process of joining
    inDB = sqlQueries.isUser(email)
    
    # send email to given email prompting them to join the confirm link to join list. 
    if(inDB):
        sqlQueries.updateUser(email, pref)

# # user is trying to join mail-list for the first time, we want to confirm their email is valid
# def join(email):
#     # check if they are already in database, if not do nothing? Or get them to restart the process of joining
#     inDB = sqlQueries.isUser(email)
    
#     # send email to given email prompting them to join the confirm link to join list. 
#     if(not inDB):
#         # its still possible for user to arrive at confirm link by just typing it in so look into preventing that
#         notify.emailConfirmation(email)


# # user has submitted form to join mailing list for the first time. 
# def confirmSignUp(email, type):
#     # convert their type into binary number
#     jobTypes = decToBin(type)
#     # Create row for them in SQL User database, email and 3 type columns
#     sqlQueries.createUser(email, jobTypes)

# # user has submitted form to update their data 
# def confirmUpdate(email, type):
#     # convert their type into binary number
#     jobTypes = decToBin(type)
#     update(email, type)

# someones or existing user is trying to update preferences 
# def update(email, type):
    
#     # check if they have  account, if so, update row in DB with new data
#     inDB = sqlQueries.isUser(email)
    
#     # send email to given email prompting them to join the confirm link to join list. 
#     if(inDB):
#         jobTypes = decToBin(type)
#         sqlQueries.updateUser(email, jobTypes)

