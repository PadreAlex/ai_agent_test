kb_docs = [
    "If you cannot find your goods by track ID, consider sending an email to support@gmail.com for assistance.",
    "Standard delivery takes 3-5 business days, while express delivery takes 1-2 business days.",
    "You can track your parcel using the tracking number provided in the confirmation email.",
    "If your package is marked as delivered but you havent received it, please check with neighbors or building security before contacting support.",
    "Returns can be initiated within 14 days of delivery using the return link in your order page.",
    "Support is available Monday through Friday from 9 AM to 6 PM. Weekend requests may be delayed.",
    "We currently deliver only within mainland areas. Deliveries to remote regions may take extra time.",
    "You can update your delivery address only before the order is marked as shipped.",
    "Damaged or missing items should be reported within 3 days of receiving the package.",
    "If your tracking status hasn't updated in over 48 hours, contact support@gmail.com with your order number.",
    "Bulk orders may require additional processing time of up to 2 business days.",
    "Deliveries may be delayed due to extreme weather or unforeseen logistic issues.",
    "Cash on delivery is only available for orders under $100.",
    "For same-day delivery, orders must be placed before 12:00 PM local time.",
    "To report any issues with your order, please use via complain_branch@gmail.com.",
]

default_human_support_error = (
    "I'm sorry, I can't answer your question. Calling for human support."
)

unexpected_human_support_error = (
    "Something unexpected happened. Calling for human support."
)

default_prefix = "Given an input question, first create a syntactically correct mssql query to run, then look at the results of the query and return the answer. Only return SQL Query not anything else like ```sql ... ```. Unless the user specifies in his question a specific number of examples he wishes to obtain, always limit your query to at most {top_k} results. Never query for all the columns from a specific table; only ask for the few relevant columns given the question. Pay attention to use only the column names that you can see in the schema description. Be careful not to query for columns that do not exist. Also, pay attention to which column is in which table. \n\n Only use the following tables: \n {table_info}\n Question: {input}."

default_suffix = "User Question: {input}\n SQL query: "

default_example_prompt = "Questions: {input}\nSQL query: {query}"

default_cant_be_answered = "unable to answer the question"
