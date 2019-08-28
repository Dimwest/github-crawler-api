# github-crawler-api

API providing statistics about Github users

## Architecture

This API was developed using one of my favorite frameworks, named Chalice (https://github.com/aws/chalice), 
a Python serverless framework based for AWS.

Here is a short description of the pros and cons of using a serverless architecture compared
to a more classic setup

#### Pros

- KISS (Keep It Simple, Stupid): removes the complexity of building and maintaining a server
- AWS Support: Chalice is built and maintained by AWS, hence totally reliable for working production systems
- Release cycles: Chalice considerably speeds up development cycles via features such as "chalice local", which enables quick debugging 
- Pricing: until a certain threshold, AWS Lambda invocations will probably be cheaper than maintaining 
non-free-tier EC2 instance
- Scalability: Lambdas can easily scale concurrent executions 
- Easy CI integration
- Monitoring: AWS Chalice automatically creates Cloudwatch log groups and streams on deploy
		
#### Cons: 

- Not integrated in an Infrastructure as Code tool (e.g. Terraform, Cloudformation), which can be problematic
when working in an environment which is 100% managed via IaC as both local and CI user must have 
IAM permissions to deploy the Lambdas
- Lambdas timeout after 15 minutes, which can be problematic for very large workloads such as 
fetching all of Facebook's repositories'. However API Gateway times out much faster hence Lambdas
will not be the bottleneck in the context of an API development

## How to

### Local deployment for testing

Note: this project currently only works on Python 3.6 and older due to an open issue on the PyGithub 
library: https://github.com/PyGithub/PyGithub/issues/856. Using the Python3.6 Docker image prevents
us from running into such compatibility issues.

Here are the commands to run in order to deploy the API in a local Docker container:

1) Run `docker build -t github-api-crawler --build-arg TOKEN=your_github_api_token .`

2) Run `docker run -d --name github-api-container github-api-crawler`

3) Enter the container shell using `docker exec -it github-api-container /bin/bash`

4) Test an API query for a specific user using `curl http://127.0.0.1:8000/monthly_new_contributors/Dimwest`

### Remote deployment on AWS

Remote deployment on AWS can be done using the `chalice deploy --stage your_stage_name` command,
after editing the security groups, subnets, and policy files required in .chalice/ directory (currently
there parameters are filled with dummy data).

Your Github API token also needs to be whether directly added in the AWS console as an environment 
variable available to the Lambda function or as a secret in AWS Secrets Manager with the following format:
`{"github_api_token": "your_github_api_token"}`
