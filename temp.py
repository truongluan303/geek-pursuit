from geek_pursuit.utils.webdriver_helper import generate_driver


url = "https://www.linkedin.com/company/gustohq"


driver = generate_driver()


driver.get(url)
htmlSource = driver.page_source
print(htmlSource)

# with open('tempfile.html', 'w') as f:
#     f.write(htmlSource)

driver.get("https://www.youtube.com/watch?v=H5WSfTknRls&ab_channel=BernardMwanza")


# driver.get(url)
# htmlSource = driver.page_source

driver.close()
