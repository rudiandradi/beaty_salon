from DB import query


def create_user_table():
    action = query("CREATE TABLE public.users"
                   "(user_id uuid PRIMARY KEY NOT NULL,"
                   "chat_id integer,"
                   "username text,"
                   "first_name text,"
                   "last_name text,"
                   "join_date timestamp with time zone,"
                   "contact text)");
    return action

def create_feedback_table():
    action = query("CREATE TABLE public.feedbacks"
                   "(user_id uuid PRIMARY KEY NOT NULL,"
                   "chat_id integer,"
                   "mark INTEGER,"
                   "comment text,"
                   "date_time timestamp with time zone)");
    return action

def create_mailing():
    action = query("CREATE TABLE public.mailing"
                   "(chat_id integer PRIMARY KEY NOT NULL,"
                   "date_time timestamp with time zone)");
    return action


#create_user_table()
#create_feedback_table()
#create_mailing()