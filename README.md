# mm-slack

mm-slack enables the `/mm [query]` slack command. 

## How it works

1. When a user types `/mm [query]` in slack, slack sends a POST request to a Tornado web server
1. The server sends the query to the MindMeld Couch Potato demo
1. The server then posts the results back to slack
