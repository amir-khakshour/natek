# naontek Goods 
## How to install
You can install this package on your local system or on a docker container. 

### Install on your local machine without docker:
1- Make sure that you have python3.5 and pip3 installed on your local machine.

2- Run the following command:
```bash
make local_setup
```

3- you can access the local server browsing to the following URL:
```text
http://127.0.0.1:8080/v1/docs/
```

### Install on a docker container:
1- install docker:
```text
https://docs.docker.com/install/
```
2- Run the following commands:
```bash
make src_image
docker run -it --name nano-web -p 8888:8080 nanotek
```
3- All endpoints are documented using swagger UI:
```text
http://127.0.0.1:8080/v1/docs/
```

### How to do actions on endpoints:
1- first you need to authenticate yourself using `/v1/api-token-auth/` endpoint:
```bash
curl -X POST "http://127.0.0.1:8080/v1/api-token-auth/" -H "accept: application/json" -H "Content-Type: application/json" -H "X-CSRFToken: RrZn24hz8Q7fSIxriRSI9Ct1eVRrUwAnSw3rDcly7oNXRgmO8ytu4wLSQvOFg9rS" -d "{ \"username\": \"root\", \"password\": \"root\"}"
```

2- Now in order to access protected api urls you must include the Authorization: JWT <your_token> header.
```bash
curl -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMSwidXNlcm5hbWUiOiJyb290IiwiZXhwIjoxNTgxNDE5MTIwLCJlbWFpbCI6ImtoYWtzaG91ci5hbWlyQGdtYWlsLmNvbSJ9.tt80vXCmnzrb9wWjxu6tfBcsZPrLeOpST70XeTtleSU" http://127.0.0.1:8080/protected-url/
curl -X DELETE "http://127.0.0.1:8080/v1/goods/product/4/" -H "accept: application/json" -H "Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMSwidXNlcm5hbWUiOiJyb290IiwiZXhwIjoxNTgxNDE5NDcxLCJlbWFpbCI6ImtoYWtzaG91ci5hbWlyQGdtYWlsLmNvbSJ9.630sWCt3YI-yUSCgoC0kXeXrjqQu8tRECyehCjDfJHw"


```

