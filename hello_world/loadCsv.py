from db_util import make_conn, fetch_data
import regex as re
import codecs
import urllib3 as urllib
import boto3
import csv

column_names = [
    'agency_code',
    'writing_company',
    'agency_name1',
    'agency_name2',
    'agency_address_line1',
    'agency_address_line2',
    'agency_city',
    'agency_state',
    'agency_zip_code',
    'agency_phone_number',
    'agency_contact_name',
    'pl_cancel_date',
    'cancel_renewal_date',
    'other_agent1',
    'other_agent2',
    'cl_cancel_date',
    'reinstatement_effec_date',
    'dl_ind_personal_auto',
    'dl_ind_homeowners',
    'dl_ind_dwelling_fire',
    'dl_ind_personal_umb',
    'dl_ind_claims',
    'dl_ind_direct_bill',
    'dl_ind_bop',
    'dl_ind_contractors',
    'dl_ind_general_liability',
    'dl_ind_commercial_auto',
    'dl_ind_workers_comp',
    'dl_ind_commercial_umb',
    'suppress_agent_dec_au',
    'suppress_agent_dec_ho',
    'suppress_agent_dec_df',
    'suppress_agent_dec_pu',
    'suppress_agent_dec_bop',
    'suppress_agent_dec_ct',
    'suppress_agent_dec_im',
    'suppress_agent_dec_ca',
    'suppress_agent_dec_wc',
    'suppress_agent_dec_cu',
    'machine_address',
    'account',
    'userid',
    'contract',
    'last_upd_date',
    'last_upd_time',
]


def lambda_handler(event, context):
    with make_conn() as conn:
        
        s3 = boto3.resource(
        service_name='s3',
        aws_access_key_id = 'AKIA45QI5CGSSVCXLNPM',
        aws_secret_access_key = 'lTdTQy05lNx6+XEY5xEuEsbtlljlNltrFIAnF+tw',
        region_name = 'us-east-2'
        )
        
        obj = s3.Bucket('sam-app-bucket1-18nplvo8sfoyn').Object('sample.csv').get()

        stream = codecs.getreader('utf-8')(obj["Body"])
        
        with conn.cursor() as cur:
            reader = csv.reader(stream)
            for row in reader:
                cols = [x.strip() for x in row] #strip whitespace
                try:
                    cur.execute(
                        'INSERT INTO agency_downloads_staging ({}) VALUES({})'.format(
                                ','.join(x for x in column_names),
                            ','.join('%s' for x in column_names)
                        ),
                        cols)
                    
                except Exception as e:
                    print(e)
                finally:
                    conn.commit()