# 🚀 GeekPursuit - Job Posting API
A REST API enabling developers to get scraped job positing data easily by just sending in GET requests. No authentication needed as well.

![scrape](https://media.giphy.com/media/xUPJPuBSBM4GEMb7Ec/giphy.gif)

I have made this a REST API instead of a library so that it is not limited to the Python programming language. I have found more popular languages such as Python, JavaScript, etc to have a lot of libraries for literally anything. However, for other less popular and probably lower-level languages, sometimes it feels like there are not enough libraries to help developers out. So I think making an API will prevent us from being blocked by the "language boundaries" :D

---

## What Can You Do With It?
![show-me](https://media.giphy.com/media/iibEPf8xEDTedJcDJr/giphy.gif)

---

### Get Job Information

You can send a `GET` request with a param `job_url_or_id` to receive the basic information including about a job post.

Example requests:

- With a job ID param: https://geek-pursuit.herokuapp.com/linkedin/job-info?job_url_or_id=3210916383

- With a URL to a direct job post: https://geek-pursuit.herokuapp.com/linkedin/job-info?job_url_or_id=https://www.linkedin.com/jobs/view/3207726319/

- With a URL to a current job in a job list: https://geek-pursuit.herokuapp.com/linkedin/job-info?job_url_or_id=https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3202709906

The API should also work even with query parameters in the URL. So there's a good chance you don't have to clean up the LinkedIn job URL before using it. A successfully returned payload should have this format:

- __title__: the position's title,
- __company__: the company's name,
- __summary__: the position's summary,
- __location__: the location of this position,
- __posted_time_ago__: indicates how long the job has been posted,
- __company_pic_url__: link to the company's logo,
- __url__: the url to the directly view the job post

Here is an example successful payload:
```json
{
  "success": true,
  "data": [
    {
      "company": "HDR",
      "title": "Application Developer",
      "company_pic_url": "https://media-exp1.licdn.com/dms/image/C560BAQGfpTq19zKb0g/company-logo_100_100/0/1560873606208?e=1668038400&v=beta&t=Sqi9J0ca-pk5j5yop83ZtE-zuYCJOs8EL6b3OszhtU0",
      "summary":"HDR hiring Application Developer in Chandler, Arizona, United States | LinkedIn",
      "description": "\n\n**_About Us  \n  \n_** At HDR, we specialize in engineering, architecture, environmental...",
      "location": "Chandler, AZ",
      "posted_time_ago": "6 hours ago",
      "url": "https://www.linkedin.com/jobs/view/3210916383/"
    }
  ]
}
```

---

### Coming Soon!

- Endpoint to get LinkedIn profile information from URL or profile ID
- Endpoint to get LinkedIn company information from URL or company ID

---

### Developer Setup
Check out [setup doc](./docs/setup.md) for more information
