def find_embed_color(course_prefix: str):
    import json

    with open('groups.json') as codes:
        data = json.load(codes)

    for college_name, college_data in data.items():
        if course_prefix in college_data['codes']:
            return college_data['color']
    return 0x00008B

def get_default_term():
    import datetime

    today = datetime.date.today()
    year = today.year
    month = today.month

    if(month > 10) or (month < 4):
        if(month > 10):
            return str((year+1))+"10"
        elif(month < 4):
            return str(year)+"10"
    else:
        return str(year)+"40"

def get_term(term: str):
    if term == "": return get_default_term()
    try:
        session, year = term.split(maxsplit=1)

        if(session == "Fall"):
            return year+"40"
        elif(session == "Summer"):
            return year+"30"
        elif(session == "Spring"):
            return year+"10"
        else:
            return get_default_term()
    except:
        print("An error in get_term() occured with '" + term + "', returning default term")
        return get_default_term()

def get_secret():
    import boto3
    from botocore.exceptions import ClientError    

    secret_name = "DiscordToken"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    return secret