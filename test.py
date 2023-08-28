a = "https://www.ebay.com/sch/i.html?_from=R40&_ipg=120&_nkw=lego&_sacat=0&LH_TitleDesc=0"
def antipagination(url):
    b = a.split("&")
    new_url = ""
    page_counter = False
    for particle in b:
        if particle.find("_ipg") != -1:
            particle = "_ipg=240"
            page_counter = True
        if new_url == "":
            new_url = particle
        else:
            new_url = new_url + "&" + particle
    if page_counter:
        return new_url
    else:
        return new_url+"&_ipg=240"

print(antipagination(a))