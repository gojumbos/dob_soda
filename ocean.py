
class OceanWrapper:
    def __init__(self):


        return



    def get_all_email_addresses(self ,):
        """ log in as admin, get all email addresses """
        emails = []
        response = self.sb_client.table('all_users').select("email_address").execute()
        emails = [list(d.values())[0] for d in response.data]  # list of dicts
        return emails