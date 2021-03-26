# stalelettuce

Hello!

stalelettuce is a package that was designed for exploring LeafLink's Redshift clusters from a Jupyter notebook quickly and easily with minimal code.

To access Redshift with stalelettuce, you have two options when initializing the Redshift object:

1.) Enter the login credentials, endpoint, and port number manually as arguments that are passed to the Redshift object.
2.) Store this information in environment variables on your machine locally.

Note: Either way, you'll need to provide the name of the database that you would like to access. 

If option number two above appeals to you then you will need to update .bashrc with the following information:

export REDSHIFT_ENDPOINT=<the AWS endpoint for the Redshift cluster>
export PORT=<the port number for the Redshift host>
export REDSHIFT_USER=<your Redshift username>
export REDSHIFT_PASS=<your Redshift password>

Note: if you need to update your shell to bash, use the following command: exec bash. Additionally, you can update your preferences under "Shell opens with" by going to "Preferences" from the terminal menu. Lastly, to find the relevant AWS credentials, check 1password. To find the endpoint and port number, go to the AWS Console.

If you would like to see additional utilities added to stalelettuce then feel free to reach out to Mike Letts on Slack! Don't worry if your idea relates to a service other than Redshift. The whole point of stalelettuce is to make data analysis faster and easier, so all ideas are welcome!
