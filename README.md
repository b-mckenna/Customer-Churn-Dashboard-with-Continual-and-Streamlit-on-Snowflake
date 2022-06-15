# Building a Churn Insights Dashboard with Continual and Streamlit on Snowflake

In this tutorial, we’re going to build an interactive customer Churn Insights Dashboard using the open-source Python framework, Streamlit, and the Continual predictions generated in [Part 1: Snowflake and Continual Quickstart Guide](https://continual.ai/post/snowflake-and-continual-quickstart-guide). In Part 1, we connected Continual to Snowflake and used a simple dataset of customer information, activity, and churn status to build and operationalize a machine learning model in Continual to predict the likelihood of a customer churning. If you haven’t completed the Quickstart Guide, I encourage you to bookmark this page and follow the guide to create the predictions. 

Customer churn is a vital business metric and often one of the first to be tracked at early-stage startups. It doesn’t take long for a business to build enough history to begin accurately predicting which customers are most likely to churn. But making predictions isn’t enough. Data teams must expose this information with context to business stakeholders. Armed with this intel, go-to-market teams can spring into action and earn their customer’s loyalty and retention. As an AI layer for the modern data stack, Continual makes it easy to operationalize predictions in multiple ways, for example through reverse ETL solutions or via any data warehouse connected application. Today’s focus will be on using Streamlit to build a custom data app, in this case a customer churn insights dashboard, to inform business decisions that can prevent churn before it happens. 

This step-by-step tutorial will provide all the code snippets necessary to create a simple Customer Churn Dashboard using Continual’s predictions. You can either create the app by following along step-by-step or you can fork or clone the Github repo, modify the Snowflake queries to include your database and table, and add your own Snowflake connection credentials. 

# What is Streamlit? 
Streamlit is a free, open-source Python app framework that enables data scientists to quickly build interactive dashboards and machine learning web apps. Streamlit understands better than any other app framework that data people aren’t front end engineers. Rather than supporting a breadth of functionality, features, and extensions, users can write lines of Python code and use the Streamlit’s API to create the essential elements data people want to present. Users can style data, draw charts and maps, add interactive widgets, cache computation, define themes, and much more. Streamlit data apps are built like a Python script: line-by-line and top to bottom. 

Building a data app is one thing, but deploying to production can be a long, cumbersome process. Streamlit makes it easy to deploy straight from Github, in a single click. And it’s getting even better. 

Since its acquisition of Streamlit, Snowflake has been working on making it even easier to build and deploy Streamlit apps. Native integration between Snowflake and Streamlit was announced at the 2022 Snowflake Summit and it won’t be long before users will be able to write Python code in Snowflake Snowsight’s Worksheets and deploy and host the app directly on a Snowflake Virtual Warehouse. 

This is only an initial taste of how Streamlit is quickly evolving to work seamlessly with Snowflake datasets, Virtual Warehouses, and collaboration features. These advancements are driving towards a future where machine learning use cases can be implemented, end-to-end, in a few hours. 

Let’s get started. 
