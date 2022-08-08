# 🚀 [in]API
A REST API enabling developers to get scraped data from LinkedIn.

![scrape-gif](https://media.giphy.com/media/xT3i0OI0a48KSslgsw/giphy.gif)

---

# Functionalities

### Get Job Information

Endpoint: https://linkedin-scrape-api.herokuapp.com/job-info

You can send a `GET` request with a param `job_url_or_id` to receive the basic information including about a job post.

Example requests:

- With a job ID param: https://linkedin-scrape-api.herokuapp.com/job-info?job_url_or_id=3210916383

- With a URL to a direct job post: https://linkedin-scrape-api.herokuapp.com/job-info?job_url_or_id=https://www.linkedin.com/jobs/view/3207726319/

- With a URL to a current job in a job list: https://linkedin-scrape-api.herokuapp.com/job-info?job_url_or_id=https://www.linkedin.com/jobs/collections/recommended/?currentJobId=3202709906

The API should also works even with query parameters in the URL. So there's a good chance you don't have to clean up the URL before using it.

A successful returned value should have this format:

- title: the position's title,
- company: the company's name,
- summary: the position's summary,
- location: the location of this position,
- posted_time_ago: indicates how long the job has been posted,
- company_pic_url: link to the company's logo,
- url: the url to the directly view the job post

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

### Developer Setup
Check out [setup doc](./docs/setup.md) for more information
