# The Crypto Tracker experiment
Crypto tracker continuously monitors Crypto assets on FTX of your choice, evaluates them against your chosen strategy, and sends you notifications on e-mail, Slack, or Discord.




## How to work with Crypto tracker 

### `databutton start`
Starts the development server.
Open [http://localhost:8000](http://localhost:8000) to view it in your browser.

The page will reload when you make changes.

### `databutton deploy`
Deploy your project on databutton.com.
Note that in order to deploy you need a user and a project in Databutton.

### `databutton build`
Builds and bundles the project, will generate all necessary files for production.\
This is automatically done when running `databutton deploy`, so it should only be necessary if you're deploying to your own infrastructure.

## How to add your own strategies
Strategies are buy, sell, or wait, signals that are emitted through evaluation one function in strategies.py. So, to add you own logic, just add one more function in there, but remember to also add the decorator. 


## Learn more

You can learn more in the [Databutton documentation](https://docs.databutton.com)
