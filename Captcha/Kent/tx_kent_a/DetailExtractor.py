import urllib
import pandas as pd
import os, csv, re, json
import pyodbc
import sqlalchemy
from scrapy.http import HtmlResponse

class DetailsData:
    JOBID = ""
    parcel_id = ""
    property_address = ""
    property_use_code = ""
    owner_name = ""
    legal_description = ""
    sales_filepath = ""

    def __init__(self, page, response, jobid, index, job_id_output_path):
        response = HtmlResponse(url='https://www.example.com',body=page.content().encode('utf-8'))
        self.index = index
        self.path = job_id_output_path
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.JOBID = jobid
        try:
            self.owner_name = '|'.join(i.strip() for i in response.xpath('//*[contains(text(),"Owner")]/../text()').getall()).strip().replace('|||||','').replace('||||', '').replace('|||','').replace("||",'').replace("|",'', 1)
            # self.owner_name = ' '.join(i.strip() for i in response.xpath('//*[contains(text(),"Owner")]/../text()').getall()).strip()
        except:
            pass
        self.property_data(response)
        # time.sleep(2)
        # self.sale_history(response)

        try:
            try:
                sales_data = len(response.xpath(
                    '//h3[contains(text(),"Document/Transfer/Sales History")]/following-sibling::div//table/thead/following-sibling::tbody/tr').getall())
            except:
                sales_data = 0
            if sales_data >= 1:
                self.sale_history(response)
                df1 = pd.read_csv(self.sales_filepath,
                                  usecols=['Instrument_number', 'book_page', 'sale_date', 'deed_type', 'V_I', 'sales_prices', 'Grantor', 'Grantee', 'Red_flag']
                )
                all_data = []
                grantee = self.owner_name
                print(grantee)
                for i, r in df1.iterrows():
                    jid = self.JOBID
                    stc = "Nv_eureka_a"
                    sales_date = r["sale_date"]
                    sales_price = r["sales_prices"]
                    doctype = r["deed_type"]
                    instnum = r['Instrument_number']
                    bkpg = str(r["book_page"])
                    grantr = str(r["Grantor"])
                    grantee = str(r["Grantee"])
                    all_data.append([jid, stc, sales_date, sales_price, doctype, instnum, bkpg, grantr, grantee])
                print(all_data[0])
                df_res = pd.DataFrame(all_data)
                df_res = df_res.fillna('')
                df_res = df_res.replace('nan', '')
                print("started pyodbc sales")
                params = urllib.parse.quote("Driver={SQL Server};Server=51.81.185.205;Database=county_search;"
                                            "UID=sa;PWD=ida@#2021;Trusted_Connection=no;")
                cnxn = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
                df_res.columns = ['Job ID', 'ST-COUNTY', 'Sales Date', 'Sales Price', 'Doctype', 'Instrument Number',
                                  'Book/Page', 'Grantor', 'Grantee']
                df_res.to_sql("SalesInformation", cnxn, if_exists='append', index=False)
        except Exception as e:
            print(e)
            pass
        try:
            print("started pyodbc prop")
            cnxn = pyodbc.connect(
                "Driver={SQL Server};Server=51.81.185.205;Database=county_search;UID=sa;PWD=ida@#2021;Trusted_Connection=no;")
            mscursor = cnxn.cursor()
            mscursor.execute("INSERT INTO PropertyInformation VALUES(?,?,?,?,?,?,?)", (
                self.JOBID, "nv_eureka_a", self.parcel_id, self.property_address, self.property_use_code,
                self.owner_name,
                self.legal_description))
            mscursor.commit()
        except:
            print("started pyodbc properror")
            pass

    def property_data(self, response):
        try:
            self.outname = self.path + f"\\Property_Summary_{self.index}.csv"
            if not os.path.exists(self.outname):
                with open(self.outname, "w", newline="") as wd:
                    wr = csv.writer(wd)
                    wr.writerow(
                        ['parcel_id', 'Owner', 'property_address', 'Tax_District', 'Block', 'lot', 'section',
                         'Township','Range', 'Map_Parcel', 'Lineage', 'Plat_Maps', 'legal_desc', 'use_code']
                    )
                wd.close()

            parcel_id = response.xpath('//section/h1/text()').get(default='').split()[-1].strip()
            Owner = self.owner_name
            try:
                # property_address = response.xpath('//th[contains(text(),"Location")]/../td/text()').getall()
                property_address = ' '.join(i.strip() for i in response.xpath('//th[contains(text(),"Location")]/../td/text()').getall()).strip()
            except:
                property_address = ''
            Tax_District = response.xpath('//th[contains(text(),"Tax District")]/../td/a/text()').get(default='').strip()
            Block,lot ='',''
            try:
                try:
                    Block_lot = response.xpath('//th[contains(text(),"Block/Lot")]/../td/text()').get(default='').strip().split("/")
                    if len(Block_lot) == 2:
                        Block = Block_lot[0]
                        lot = Block_lot[1]
                    else:
                        Blo_lot = response.xpath('//th[starts-with(text(),"Block")]/../td/text()').get(
                            default='').strip()
                        Block = Blo_lot

                except:
                    pass
                # try:
                #     Blo_lot = response.xpath('//th[contains(text(),"Block")]/../td/text()').get(default='').strip()
                #     Block = Blo_lot
                # except:
                #     pass
            except:
                pass
            section = response.xpath('//th[contains(text(),"Section")]/../td/text()').get(default='').strip()
            Township = response.xpath('//th[contains(text(),"Township")]/../td/text()').get(default='').strip()
            Range = response.xpath('//th[contains(text(),"Range")]/../td/text()').get(default='').strip()
            Map_Parcel = response.xpath('//th[contains(text(),"Map Parcel")]/../td/text()').get(default='').strip()
            Lineage = response.xpath('//th[contains(text(),"Lineage")]/../td/a/text()').get(
                default='').strip()
            Plat_Maps = response.xpath('//th[contains(text(),"Plat Maps")]/../td/a/text()').get(
                default='').strip()
            legal_desc = response.xpath('//h3[contains(text(),"Land Lines")]/../div//tr/th[contains(text(),"Description")]/../../following-sibling::tbody/tr/td[2]/text()').get(default="").strip()
            use_code = response.xpath('//th[contains(text(),"Use Code")]/../td/a/text()').get(
                default="").strip()
            self.parcel_id = parcel_id
            self.property_address = property_address
            self.legal_description = legal_desc
            self.property_use_code = use_code

            alldata = [parcel_id, self.owner_name, property_address, Tax_District, Block, lot, section, Township, Range,Map_Parcel,
                       Lineage, Plat_Maps, legal_desc,use_code]
            with open(self.outname, "a", newline="") as wd:
                wr = csv.writer(wd)
                print(f'["ALLDATA"]>>>{alldata}')
                wr.writerow(alldata)
                wd.close()
        except:
            pass

    def sale_history(self, response):
        try:
            self.sales_filepath = self.path + f"\\sales_history_{self.parcel_id}.csv"
            rows = response.xpath('//h3[contains(text(),"Document/Transfer/Sales History")]/following-sibling::div//table/thead/following-sibling::tbody/tr').getall()
            print("saleshistory_count:",len(rows))
            if not os.path.exists(self.sales_filepath):
                with open(self.sales_filepath, "w", newline="") as wd:
                    wr = csv.writer(wd)
                    wr.writerow(
                        ['Instrument_number', 'book_page', 'sale_date', 'deed_type', 'V_I', 'sales_prices', 'Grantor', 'Grantee', 'Red_flag']
                        )
                wd.close()
            allsales_data = []
            for i in range(1, len(rows)+1):
                Instrument_number,book_page = '', ''
                try:
                    bp = response.xpath(f'//th[contains(text(),"Official Record")]/../../following-sibling::tbody/tr[{i}]/td[2]/a/text()').get(default='').strip()
                    if "BK" in bp:
                        bk = bp.split()[0].replace("BK:", '')
                        pg = bp.split()[1].replace("PG:", '')
                        book_page = bk + "/" + pg
                    else:
                        Instrument_number = bp
                except:
                    pass
                try:
                    sale_date_1 = response.xpath(f"//th[contains(text(),'Date')]/../../following-sibling::tbody/tr[{i}]/td[3]/text()").get(default='').strip()
                    a = sale_date_1.split("-")[1]
                    b = sale_date_1.split("-")[2]
                    c = sale_date_1.split("-")[0]
                    sale_date = a + "/" + b + "/" + c
                except:
                    sale_date =''
                deed_type = response.xpath(f"//th[contains(text(),'Type')]/../../following-sibling::tbody/tr[{i}]/td[4]/a/text()").get(default='').strip()
                V_I = response.xpath(f"//th[contains(text(),'Type')]/../../following-sibling::tbody/tr[{i}]/td[5]//text()").get(default='').strip()
                sales_prices = response.xpath(f"//th[contains(text(),'Type')]/../../following-sibling::tbody/tr[{i}]/td[6]//text()").get(default='').strip()
                Grantor,Grantee ='', ''
                try:
                    Grant = response.xpath(f'//th[contains(text(),"Ownership")]/../../following-sibling::tbody/tr[{i}]/td[7]/text()').getall()
                    if len(Grant)==1:
                        Grantee = Grant[0]
                        print(Grantee)
                    if len(Grant)==2:
                        Grantor = Grant[0]
                        Grantee = Grant[1]
                except:
                    Grantee =''
                    Grantor = ''
                Red_flag = response.xpath(f"(//th[contains(text(),'Type')]/../../following-sibling::tbody/tr[{i}]/td[8])[1]/text()").get(default='').strip()

                rows_data = [Instrument_number,book_page.replace('nan',''), sale_date, deed_type, V_I,sales_prices,Grantor,Grantee,Red_flag]
                allsales_data.append(rows_data)
                with open(self.sales_filepath, "a", newline="") as wd:
                    wr = csv.writer(wd)
                    print(f'["SALES_ALLDATA"]>>>{rows_data}')
                    wr.writerow(rows_data)
                    wd.close()
        except:
            pass

# class DetailsData:
#     JOBID = ""
#     parcel_id = ""
#     property_address = ""
#     property_use_code = ""
#     owner_name = ""
#     legal_description = ""
#     sales_filepath = ""
#
#     def __init__(self, page, response, jobid, index, job_id_output_path):
#         response = HtmlResponse(url='https://www.example.com',body=page.content().encode('utf-8'))
#         self.index = index
#         self.path = job_id_output_path
#         if not os.path.exists(self.path):
#             os.makedirs(self.path)
#         self.JOBID = jobid
#         try:
#             self.owner_name = '|'.join(i.strip() for i in response.xpath('//*[contains(text(),"Owner")]/../text()').getall()).strip().replace('|||||','').replace('||||', '').replace('|||','').replace("||",'')
#         except:
#             pass
#         self.property_data(response)
#         page.wait_for_timeout(timeout=3000)
#         self.sale_history(response)
#
#         # try:
#         #     try:
#         #         sales_data = len(response.xpath(
#         #             '//h3[contains(text(),"Document/Transfer/Sales History")]/following-sibling::div//table/thead/following-sibling::tbody/tr').getall())
#         #     except:
#         #         sales_data = 0
#         #     if sales_data > 1:
#         #         self.sale_history(response)
#         #         df1 = pd.read_csv(self.sales_filepath,
#         #                           usecols=['Instrument_number', 'book_page', 'sale_date', 'deed_type', 'V_I', 'sales_prices', 'Grantor', 'Grantee', 'Red_flag']
#         #         )
#         #         all_data = []
#         #         grantee = self.owner_name
#         #         print(grantee)
#         #         for i, r in df1.iterrows():
#         #             jid = self.JOBID
#         #             stc = "Nv_douglas_a"
#         #             sales_date = r["sale_date"]
#         #             sales_price = r["sales_prices"]
#         #             doctype = r["deed_type"]
#         #             instnum = r['Instrument_number']
#         #             bkpg = str(r["book_page"])
#         #             grantr = str(r["Grantor"])
#         #             grantee = str(r["Grantee"])
#         #             all_data.append([jid, stc, sales_date, sales_price, doctype, instnum, bkpg, grantr, grantee])
#         #         print(all_data[0])
#         #         df_res = pd.DataFrame(all_data)
#         #         df_res = df_res.fillna('')
#         #         print("started pyodbc sales")
#         #         params = urllib.parse.quote("Driver={SQL Server};Server=51.81.185.205;Database=county_search;"
#         #                                     "UID=sa;PWD=ida@#2021;Trusted_Connection=no;")
#         #         cnxn = sqlalchemy.create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
#         #         df_res.columns = ['Job ID', 'ST-COUNTY', 'Sales Date', 'Sales Price', 'Doctype', 'Instrument Number',
#         #                           'Book/Page', 'Grantor', 'Grantee']
#         #         df_res.to_sql("SalesInformation", cnxn, if_exists='append', index=False)
#         # except Exception as e:
#         #     print(e)
#         #     pass
#         # try:
#         #     print("started pyodbc prop")
#         #     cnxn = pyodbc.connect(
#         #         "Driver={SQL Server};Server=51.81.185.205;Database=county_search;UID=sa;PWD=ida@#2021;Trusted_Connection=no;")
#         #     mscursor = cnxn.cursor()
#         #     mscursor.execute("INSERT INTO PropertyInformation VALUES(?,?,?,?,?,?,?)", (
#         #         self.JOBID, "nv_douglas_a", self.parcel_id, self.property_address, self.property_use_code,
#         #         self.owner_name,
#         #         self.legal_description))
#         #     mscursor.commit()
#         # except:
#         #     print("started pyodbc properror")
#         #     pass
#
#     def property_data(self, response):
#         try:
#             self.outname = self.path + f"\\Property_Summary_{self.index}.csv"
#             if not os.path.exists(self.outname):
#                 with open(self.outname, "w", newline="") as wd:
#                     wr = csv.writer(wd)
#                     wr.writerow(
#                         ['parcel_id', 'Owner', 'property_address', 'Tax_District', 'Block', 'lot', 'section',
#                          'Township','Range', 'Map_Parcel', 'Lineage', 'Plat_Maps', 'legal_desc', 'use_code']
#                     )
#                 wd.close()
#
#             parcel_id = response.xpath('//section/h1/text()').get(default='').split()[-1].strip()
#             Owner = ''
#             try:
#                 owner_name = '|'.join(i.strip() for i in response.xpath('//*[contains(text(),"Owner")]/../text()').getall()).strip().replace('|||||','').replace('||||', '').replace('|||','').replace("||",'')
#                 print(owner_name)
#             except:
#                 pass
#             try:
#                 property_address = response.xpath('//th[contains(text(),"Location")]/../td/text()').get(default='').strip()
#             except:
#                 property_address = ''
#             Tax_District = response.xpath('//th[contains(text(),"Tax District")]/../td/a/text()').get(default='').strip()
#             Block,lot ='',''
#             try:
#                 try:
#                     Block_lot = response.xpath('//th[contains(text(),"Block/Lot")]/../td/text()').get(default='').strip().split("/")
#                     if len(Block_lot)==2:
#                         Block = Block_lot[0]
#                         lot = Block_lot[1]
#                 except:
#                     pass
#                 try:
#                     Blo_lot = response.xpath('//th[contains(text(),"Lot")]/../td/text()').get(default='').strip()
#                     lot = Blo_lot
#                 except:
#                     pass
#             except:
#                 pass
#             section = response.xpath('//th[contains(text(),"Section")]/../td/text()').get(default='').strip()
#             Township = response.xpath('//th[contains(text(),"Township")]/../td/text()').get(default='').strip()
#             Range = response.xpath('//th[contains(text(),"Range")]/../td/text()').get(default='').strip()
#             Map_Parcel = response.xpath('//th[contains(text(),"Map Parcel")]/../td/text()').get(default='').strip()
#             Lineage = response.xpath('//th[contains(text(),"Lineage")]/../td/a/text()').get(
#                 default='').strip()
#             Plat_Maps = response.xpath('//th[contains(text(),"Plat Maps")]/../td/a/text()').get(
#                 default='').strip()
#             legal_desc = response.xpath('//h3[contains(text(),"Land Lines")]/../div//tr/th[contains(text(),"Description")]/../../following-sibling::tbody/tr/td[2]/text()').get(default="").strip()
#             use_code = response.xpath('//th[contains(text(),"Use Code")]/../td/a/text()').get(
#                 default="").strip()
#             self.parcel_id = parcel_id
#             self.property_address = property_address
#             self.legal_description = legal_desc
#             self.property_use_code = use_code
#
#             alldata = [parcel_id, self.owner_name, property_address, Tax_District, Block, lot, section, Township, Range,Map_Parcel,
#                        Lineage, Plat_Maps, legal_desc,use_code]
#             with open(self.outname, "a", newline="") as wd:
#                 wr = csv.writer(wd)
#                 print(f'["ALLDATA"]>>>{alldata}')
#                 wr.writerow(alldata)
#                 wd.close()
#         except:
#             pass
#
#     def sale_history(self, response):
#         try:
#             self.sales_filepath = self.path + f"\\sales_history_{self.parcel_id}.csv"
#             rows = response.xpath('//h3[contains(text(),"Document/Transfer/Sales History")]/following-sibling::div//table/thead/following-sibling::tbody/tr').getall()
#             print("saleshistory_count:",len(rows))
#             if not os.path.exists(self.sales_filepath):
#                 with open(self.sales_filepath, "w", newline="") as wd:
#                     wr = csv.writer(wd)
#                     wr.writerow(
#                         ['Instrument_number', 'book_page', 'sale_date', 'deed_type', 'V_I', 'sales_prices', 'Grantor', 'Grantee', 'Red_flag']
#                         )
#                 wd.close()
#             allsales_data = []
#             for i in range(1, len(rows)+1):
#                 Instrument_number = response.xpath(f'//th[contains(text(),"Official Record")]/../../following-sibling::tbody/tr[{i}]/td[1]/a/text()').get(default='').strip()
#                 book_page = ''
#                 try:
#                     bp = response.xpath(f'//th[contains(text(),"Official Record")]/../../following-sibling::tbody/tr[{i}]/td[1]/text()').get(default='').strip()
#                     book_page_1 = bp.split('-')
#                     if len(book_page_1)==2:
#                         bk=book_page_1[0]
#                         pg=book_page_1[1]
#                         book_page= bk+"/"+pg
#                     else:
#                         book_page = bp
#                 except:
#                     pass
#
#                 try:
#                     sale_date_1 = response.xpath(f"//th[contains(text(),'Date')]/../../following-sibling::tbody/tr[{i}]/td[2]/text()").get(default='').strip()
#                     a = sale_date_1.split("-")[1]
#                     b = sale_date_1.split("-")[2]
#                     c = sale_date_1.split("-")[0]
#                     sale_date = a + "/" + b + "/" + c
#                 except:
#                     sale_date =''
#                 deed_type = response.xpath(f"//th[contains(text(),'Type')]/../../following-sibling::tbody/tr[{i}]/td[3]/a/text()").get(default='').strip()
#                 V_I = response.xpath(f"//th[contains(text(),'Type')]/../../following-sibling::tbody/tr[{i}]/td[4]//text()").get(default='').strip()
#                 sales_prices = response.xpath(f"//th[contains(text(),'Type')]/../../following-sibling::tbody/tr[{i}]/td[5]//text()").get(default='').strip()
#                 Grantor,Grantee ='', ''
#                 try:
#                     Grant = response.xpath(f'//th[contains(text(),"Ownership")]/../../following-sibling::tbody/tr[{i}]/td[6]/text()').getall()
#                     if len(Grant)==1:
#                         Grantee = Grant[0]
#                         print(Grantee)
#                     if len(Grant)==2:
#                         Grantor = Grant[0]
#                         Grantee = Grant[1]
#                 except:
#                     Grantee =''
#                     Grantor = ''
#                 Red_flag = response.xpath(f"(//th[contains(text(),'Type')]/../../following-sibling::tbody/tr[{i}]/td[7])[1]/text()").get(default='').strip()
#
#                 rows_data = [Instrument_number,book_page.replace('nan',''), sale_date, deed_type, V_I,sales_prices,Grantor,Grantee,Red_flag]
#                 allsales_data.append(rows_data)
#                 with open(self.sales_filepath, "a", newline="") as wd:
#                     wr = csv.writer(wd)
#                     print(f'["SALES_ALLDATA"]>>>{rows_data}')
#                     wr.writerow(rows_data)
#                     wd.close()
#         except:
#             pass

