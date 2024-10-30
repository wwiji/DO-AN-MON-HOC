from scr.Crawl import Get_Data
from scr.MongoDB import MongoDB
from scr.qu_ import queries
from scr.nor_data import clear_data

def main():

    # crawl data
    get_data = Get_Data(2, 3)
    get_data.get_links()
    get_data.properties()
    get_data.save_data_to_json()


    # clear data
    cl = clear_data('property_data.json', 'property_data_tr.json')
    cl.process()

    # save data to MongoDB
    mongodb = MongoDB()
    data = mongodb.read_json('property_data_tr.json')
    mongodb.insert_data(data)

    # query data
    query = queries()
    query.print_q()



#hàm main
main()