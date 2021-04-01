# stalelettuce

Hello!


stalelettuce is a package that was originally designed for exploring LeafLink's Redshift clusters from a Jupyter notebook quickly and easily with minimal code.


To access Redshift with stalelettuce, you have two options when initializing the Redshift object:


  1.) Enter the login credentials, endpoint, and port number manually as arguments that are passed to the Redshift object.</br>

  2.) Store this information in environment variables on your machine locally.


Note: You'll need to provide the name of the database that you would like to access.


If option number two above appeals to you then you will need to update .bashrc with the following information:


`export REDSHIFT_ENDPOINT=<the AWS endpoint for the Redshift cluster>`</br>
`export PORT=<the port number for the Redshift host>`</br>
`export REDSHIFT_USER=<your Redshift username>`</br>
`export REDSHIFT_PASS=<your Redshift password>`</br>


Note: if you need to update your shell to bash, use the following command: `exec bash`. Similarly, you can use `source ~/.bashrc`. Additionally, you can update your shell preferences under "Shell opens with" by going to "Preferences" from the terminal menu. Lastly, to find the relevant AWS credentials, check 1password. To find the endpoint and port number, go to the AWS Console.

Below are some use cases for stalelettuce:

```
# importing stalelettuce; aliasing as 'sl'
import stalelettuce as sl
# initializing Redshift class; assigning to 'rs' object
rs = sl.Redshift(dbname="warehouse_prod")
# use the schemas method as below to see schemas in 'warehouse_prod' database in a pandas dataframe
rs.schemas()
# use the tables method to see every schema-table pair in 'warehouse_prod' in a pandas dataframe
rs.tables()
# pass an optional schema name as an arg to the tables method to see the tables
# associated with a specific schema instead of using pandas' loc method
rs.tables(schema_name="llf_reporting")
# use the columns method to see the column names, ordinal position, and data type of every
# field in a specific table. just pass the schema and table names as args
rs.columns(schema_name="llf_reporting", table_name="transaction_all")
# use the query method to pass a query as an arg and return a pandas dataframe of the results
sql = """select count(distinct ta.seller_id) num_sellers from llf_reporting.transaction_all ta"""
rs.query(sql=sql)
```

If you would like to see additional utilities added to stalelettuce then feel free to reach out to Mike Letts on Slack! Don't worry if your idea relates to a service other than Redshift. The whole point of stalelettuce is to make data analysis at LeafLink faster and easier, so all ideas are welcome!
