from lxml import html 
import os 




file_to_parse = 'src/data/trainings.html'
html_doc = html.parse(file_to_parse)
row_ods = html_doc.xpath('//div[@class="row odd"]')
for row in row_ods:
    cell_date:str = row.xpath('.//div[@class="cell date"]')[0].text_content()
    sesion_idcr:str = row.xpath('.//input[@name="hdSessionIdCR"]')[0].attrib['id']
    href:str = row.xpath('.//div[@class="single-item clearfix even"]/a')[0].attrib['href']
    print(href)


        
    
